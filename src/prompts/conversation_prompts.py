"""
LangChain prompt templates for conversation generation.
"""

from langchain.prompts import PromptTemplate
from typing import Dict, Any


class ConversationPromptTemplates:
    """Collection of LangChain prompt templates for fraud detection conversations."""
    
    @staticmethod
    def get_conversation_generation_template() -> PromptTemplate:
        """
        Get the main conversation generation prompt template.
        
        Returns:
            PromptTemplate: LangChain prompt template for conversation generation
        """
        
        template = """You are an expert scriptwriter and fraud analyst tasked with creating a realistic phone conversation for fraud detection training. Your output must be a single, valid JSON object with the exact structure specified below.

**CRITICAL: Your response MUST be valid JSON. Use proper decimal numbers (e.g., 0.85, not "0. 85" or "zero point eight five"). Ensure all strings are properly escaped and all brackets/braces are balanced.**

**CONTEXT:**
- Agent Persona: {agent_persona}
- Customer Persona: {customer_persona}
- Scenario: {scenario_description}
- Case Type: {case_type}
- Target Duration: Approximately {duration} seconds (CRITICAL: Ensure conversation lasts close to this duration)
- Policy Rules: {policy_rules}

**CRITICAL INSTRUCTIONS:**

1. **TRANSCRIPT GENERATION:**
   - Create a natural, realistic phone conversation between the agent and customer in Indian English.
   - Incorporate common Indian English phrases and occasional simple Hindi words (e.g., 'Sir,' 'Achha,' 'Thik hai,' 'ji') to enhance realism.
   - Each dialogue line must include a "timestamp_end" field (cumulative seconds from call start)
   - The conversation MUST last approximately {duration} seconds - this is crucial for training consistency
   - Include realistic pauses, interruptions, and conversational elements
   - The agent should embody their persona, the customer should react according to their persona
   - For fraud scenarios, show the progression of the fraudulent request
   - For normal scenarios, keep the interaction professional and legitimate
   - Ensure timestamps progress naturally and reach close to {duration} seconds

2. **MULTIMODAL ANALYSIS:**
   - Analyze the overall conversation tone and generate realistic audio cues
   - Dominant emotion: primary emotional tone (e.g., "anxious", "aggressive", "calm", "urgent")
   - Secondary emotion: secondary emotional undertone
   - Pace: conversation speed (e.g., "fast", "normal", "slow", "rushed")
   - Confidence score: MUST be a valid decimal number between 0.0 and 1.0 (e.g., 0.85, 0.92, 0.75) - DO NOT use words or spaces

3. **SLOW-THINKING RATIONALE:**
   - Provide a detailed analysis explaining the final verdict
   - Reference specific policy violations or compliance points
   - Consider both verbal content and implied audio cues
   - Explain the reasoning process step-by-step

4. **VERDICT:**
   - "YES" if the conversation violates any policy rules (fraudulent)
   - "NO" if the conversation follows all policies (legitimate)

**REQUIRED JSON OUTPUT STRUCTURE:**
```json
{{
    "transcript": [
        {{
            "speaker": "Agent",
            "text": "Hello, this is calling from XYZ Bank. Am I speaking with [Customer Name]?",
            "timestamp_end": 3.5
        }},
        {{
            "speaker": "Customer", 
            "text": "Yes, this is [Customer Name]. How can I help you?",
            "timestamp_end": 6.2
        }}
    ],
    "multimodal_analysis": {{
        "dominant_emotion": "urgent",
        "secondary_emotion": "confident", 
        "pace": "fast",
        "confidence_score": 0.85
    }},
    "key_entities": {{
        "organization": ["XYZ Bank"],
        "product": ["online banking", "debit card"],
        "pii_requested": ["username", "password"]
    }},
    "chunk_level_analysis": [
        {{
            "timestamp": 10.0,
            "verdict_at_chunk": "NO",
            "rationale_at_chunk": "At 10.0s: The agent has claimed to be from the bank and mentioned account security. While this creates urgency, no policy has been violated yet."
        }},
        {{
            "timestamp": 16.0,
            "verdict_at_chunk": "YES",
            "rationale_at_chunk": "At 16.0s: The agent has explicitly asked for sensitive information that violates policy rules. This confirms fraudulent intent."
        }}
    ],
    "final_slow_thinking_rationale": "Based on the conversation analysis, the agent requested [specific analysis]. This violates/complies with [specific policy rule]. The audio cues suggest [analysis]. Therefore, the verdict is [reasoning].",
    "final_verdict": "YES",
    "violated_policies": [
        "Rule A: Agents must NEVER ask for a customer's password or full PIN."
    ],
    "scam_outcome": "Successful"
}}
```

**ADDITIONAL INSTRUCTIONS FOR NEW FIELDS:**

5. **KEY_ENTITIES:**
   - organization: List all banks, companies, or organizations mentioned
   - product: List all banking products/services mentioned
   - pii_requested: List all personal identifiable information the agent asks for
   - For normal calls with no PII requests, pii_requested should be an empty array []

6. **CHUNK_LEVEL_ANALYSIS (CRITICAL FOR REAL-TIME DETECTION):**
   - Generate verdict decisions at **EXACTLY 5-second intervals**: 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, etc.
   - Continue until the conversation duration is reached
   - Each chunk should have: timestamp, verdict_at_chunk ("YES" or "NO"), and rationale_at_chunk
   
   **CRITICAL TIMING RULE:**
   - The verdict MUST flip to "YES" in the SAME 5-second interval where the policy violation occurs
   - Example: If agent asks for OTP at timestamp 48.0, the chunk at 50.0 (covering 45-50s) MUST show verdict="YES"
   - Example: If agent asks for password at timestamp 23.0, the chunk at 25.0 (covering 20-25s) MUST show verdict="YES"
   - DO NOT delay the verdict to the next chunk - this is critical for real-time fraud detection systems
   
   **Rationale Requirements:**
   - Reference events that occurred WITHIN that chunk's 5-second window
   - For a chunk at timestamp X, analyze events that happened between (X-5) and X seconds
   - Be specific about what happened in that time window
   
   **Progression pattern:**
   - For fraud calls: Early chunks show "NO" until violation occurs, then ALL subsequent chunks are "YES"
   - For normal calls: ALL chunks should be "NO" with rationales explaining continued compliance
   
   **Example for fraud scenario:**
   ```json
   "chunk_level_analysis": [
       {{"timestamp": 5.0, "verdict_at_chunk": "NO", "rationale_at_chunk": "At 5s: Initial greeting and introduction, no policy violations yet."}},
       {{"timestamp": 10.0, "verdict_at_chunk": "NO", "rationale_at_chunk": "At 10s: Agent mentions suspicious activity, creating urgency but not yet requesting prohibited information."}},
       {{"timestamp": 15.0, "verdict_at_chunk": "NO", "rationale_at_chunk": "At 15s: Verification using DOB and last 4 digits of mobile (allowed under Rule C)."}},
       {{"timestamp": 20.0, "verdict_at_chunk": "YES", "rationale_at_chunk": "At 18s: Agent explicitly asks for OTP, directly violating Rule A. This is the moment fraud is detectable."}},
       {{"timestamp": 25.0, "verdict_at_chunk": "YES", "rationale_at_chunk": "At 25s: Agent continues to pressure customer for OTP, maintaining policy violation."}},
       {{"timestamp": 30.0, "verdict_at_chunk": "YES", "rationale_at_chunk": "At 28s: Agent also requests password, further violating Rule A. Fraud confirmed."}}
   ]
   ```

7. **VIOLATED_POLICIES:**
   - List the exact policy rules (as written in the scenario) that were violated
   - Copy the rule text verbatim from the policy section
   - For normal/compliant calls, this should be an empty array []

8. **SCAM_OUTCOME:**
   - Based on the customer persona and conversation flow, determine if the scam was successful
   - "Successful": Customer provided the requested sensitive information or took the fraudulent action
   - "Failed": Customer became suspicious and refused to comply
   - "Interrupted": Customer ended the call before completing the scammer's request
   - For normal calls, set this to "N/A"

Generate the complete conversation now, ensuring it follows the scenario, personas, and policies exactly. Output only the JSON object."""
        
        return PromptTemplate(
            input_variables=[
                "agent_persona", 
                "customer_persona", 
                "scenario_description", 
                "case_type", 
                "duration", 
                "policy_rules"
            ],
            template=template
        )
    
    @staticmethod
    def get_conversation_refinement_template() -> PromptTemplate:
        """
        Get a template for refining generated conversations.
        
        Returns:
            PromptTemplate: LangChain prompt template for conversation refinement
        """
        
        template = """Review and refine the following conversation to ensure it meets all requirements:

**Original Conversation:**
{original_conversation}

**Requirements to Check:**
1. Duration should be approximately {target_duration} seconds
2. Timestamps should progress naturally
3. Agent should exhibit: {agent_persona}
4. Customer should exhibit: {customer_persona}
5. Scenario compliance: {scenario_description}
6. Policy adherence: {policy_rules}

**Instructions:**
- If the conversation is too short, add more realistic dialogue
- If timestamps are inconsistent, fix the progression
- Ensure personality traits are clearly demonstrated
- Verify the final verdict matches the conversation content

Output the refined conversation in the same JSON format."""
        
        return PromptTemplate(
            input_variables=[
                "original_conversation",
                "target_duration",
                "agent_persona",
                "customer_persona", 
                "scenario_description",
                "policy_rules"
            ],
            template=template
        )
    
    @staticmethod
    def get_chunk_rationale_template() -> PromptTemplate:
        """
        Get a template for generating chunk-specific rationales.
        
        Returns:
            PromptTemplate: LangChain prompt template for chunk rationale generation
        """
        
        template = """Generate a concise rationale for the fraud detection verdict at timestamp {chunk_timestamp} seconds.

**Conversation so far:**
{cumulative_transcript}

**Scenario Context:**
- Case Type: {case_type}
- Policy Rules: {policy_rules}

**Current Verdict:** {verdict}

Generate a 1-2 sentence rationale explaining why the verdict is "{verdict}" at this specific timestamp. Consider:
- What has been said so far
- Whether any policy violations have occurred yet
- The progression of the conversation

Format: "At {chunk_timestamp}s: [your rationale here]"
"""
        
        return PromptTemplate(
            input_variables=[
                "chunk_timestamp",
                "cumulative_transcript", 
                "case_type",
                "policy_rules",
                "verdict"
            ],
            template=template
        )
