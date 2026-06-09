"""
Chunk expansion utilities for converting source conversations into training data.
"""

from typing import Dict, List, Any
from rich.console import Console

from config.settings import CHUNK_INTERVAL_SECONDS


class ChunkExpander:
    """Handles Stage 2: Expanding source conversations into training chunks."""

    def __init__(self, console: Console):
        self.console = console

    def expand_conversation_into_chunks(self, source_conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Stage 2: Expand a source conversation into multiple training data points.

        Processes every conversation into cumulative 3-second chunks regardless of
        case type, matching the released ICFD-31k streaming-chunk construction.

        Args:
            source_conversation: Complete conversation data from Stage 1

        Returns:
            List of training data points (chunks)
        """
        transcript = source_conversation.get("transcript", [])
        final_verdict = source_conversation.get("final_verdict", "NO")
        multimodal_analysis = source_conversation.get("multimodal_analysis", {})
        scenario = source_conversation.get("scenario", {})
        session_id = source_conversation.get("session_id", 0)

        max_timestamp = max([line.get("timestamp_end", 0) for line in transcript]) if transcript else 0
        chunk_timestamps = list(
            range(CHUNK_INTERVAL_SECONDS, int(max_timestamp) + 1, CHUNK_INTERVAL_SECONDS)
        )

        training_chunks = []
        fraud_start_time = self._find_fraud_start_time(transcript, scenario, source_conversation)

        for chunk_time in chunk_timestamps:
            cumulative_transcript = [
                line for line in transcript if line.get("timestamp_end", 0) <= chunk_time
            ]

            if not cumulative_transcript:
                continue

            if final_verdict == "NO":
                intermediate_verdict = "NO"
            else:
                intermediate_verdict = "YES" if chunk_time >= fraud_start_time else "NO"

            cumulative_audio_analysis = self._create_chunk_audio_analysis(
                cumulative_transcript, multimodal_analysis, chunk_time
            )
            intermediate_rationale = self._generate_intermediate_rationale(
                cumulative_transcript, scenario, chunk_time, intermediate_verdict
            )

            training_chunks.append({
                "session_id": session_id,
                "chunk_timestamp": chunk_time,
                "cumulative_transcript": cumulative_transcript,
                "cumulative_audio_analysis": cumulative_audio_analysis,
                "slow_thinking_rationale": intermediate_rationale,
                "final_verdict": intermediate_verdict,
                "scenario_info": {
                    "scenario_id": scenario.get("scenario_id"),
                    "case_type": scenario.get("case_type"),
                    "description": scenario.get("description"),
                },
                "combination_key": source_conversation.get("combination_key", ""),
                "multiplier_round": source_conversation.get("multiplier_round", 1),
                "generated_at": source_conversation.get("generated_at"),
            })

        return training_chunks

    def _find_fraud_start_time(
        self, transcript: List[Dict], scenario: Dict, source_conversation: Dict
    ) -> float:
        """Determine when fraudulent activity first occurs in the conversation."""
        case_type = scenario.get("case_type", "")

        if case_type in ["Clear Normal", "Ambiguous but Ultimately Normal"]:
            return float("inf")

        fraud_indicators = [
            "password", "pin", "otp", "cvv", "card number", "download", "install",
            "processing fee", "advance fee", "legal action", "account will be blocked",
            "transfer money", "send money", "share screen", "remote access", "verify",
            "confirm", "update", "urgent", "immediately", "expire", "suspend",
        ]

        for line in transcript:
            text = line.get("text", "").lower()
            if any(indicator in text for indicator in fraud_indicators):
                return line.get("timestamp_end", 0)

        if transcript:
            max_time = max([line.get("timestamp_end", 0) for line in transcript])
            return max_time * 0.6

        return 0

    def _create_chunk_audio_analysis(
        self, cumulative_transcript: List[Dict], original_analysis: Dict, chunk_time: float
    ) -> Dict:
        """Create simplified audio analysis for a specific chunk."""
        dominant_emotion = original_analysis.get("dominant_emotion", "neutral")
        secondary_emotion = original_analysis.get("secondary_emotion", "calm")
        pace = original_analysis.get("pace", "normal")
        base_confidence = original_analysis.get("confidence_score", 0.7)
        chunk_confidence = min(base_confidence + (chunk_time / 100), 1.0)

        return {
            "dominant_emotion": dominant_emotion,
            "secondary_emotion": secondary_emotion,
            "pace": pace,
            "confidence_score": round(chunk_confidence, 2),
        }

    def _generate_intermediate_rationale(
        self, cumulative_transcript: List[Dict], scenario: Dict, chunk_time: float, verdict: str
    ) -> str:
        """Generate a concise rationale for the intermediate verdict at this timestamp."""
        case_type = scenario.get("case_type", "")

        if verdict == "NO":
            if case_type == "Clear Normal":
                return (
                    f"At {chunk_time}s: Conversation remains within policy guidelines. "
                    "All requests are legitimate and follow proper procedures."
                )
            return (
                f"At {chunk_time}s: No policy violations detected yet. "
                "Conversation appears normal, continuing to monitor for suspicious activity."
            )

        return (
            f"At {chunk_time}s: Policy violation detected. Agent has made requests that "
            "breach security protocols. Conversation flagged as fraudulent."
        )
