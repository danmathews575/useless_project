import streamlit as st
import random
import json
import os
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Set page config with legal theme
st.set_page_config(
    page_title="⚖️ വീണപൂവ് - The Worst AI Lawyer",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for legal theme
st.markdown("""
<style>
    .header-section {
        background: linear-gradient(45deg, #1a472a, #0d2d1c);
        color: #f0f0c0;
        padding: 2rem;
        border-radius: 5px;
        margin-bottom: 1.5rem;
        font-family: 'Times New Roman', serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #8b5a2b;
    }
    .verdict-section {
        background-color: #f9f3e9;
        padding: 1.5rem;
        border-radius: 5px;
        border-left: 5px solid #c1121f;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    .exhibit-card {
        background: #f8f5f0;
        border: 1px solid #d4af37;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .legal-jargon {
        color: #5d4037;
        font-weight: 700;
        font-style: italic;
    }
    .stButton>button {
        background: linear-gradient(45deg, #1a472a, #0d2d1c) !important;
        color: #f0f0c0 !important;
        font-weight: bold;
        border: 1px solid #8b5a2b !important;
    }
    .stTextInput>div>div>input {
        background-color: #f9f3e9 !important;
        border: 1px solid #8b5a2b !important;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        color: #5d4037;
        font-size: 0.8rem;
    }
    .error-section {
        background-color: #ffebee;
        padding: 1.5rem;
        border-radius: 5px;
        border-left: 5px solid #c1121f;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

class Veenapuvu:
    def __init__(self):
        self.case_number = f"CV-{random.randint(2020,2025)}-{random.randint(1000,9999)}"
        self.use_gpt = False
        self.setup_gpt()
        self.load_resources()
        
    def setup_gpt(self):
        """Set up GPT functionality using secrets.toml"""
        try:
            # Check if API key exists in secrets
            if 'OPENAI_API_KEY' in st.secrets:
                os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
                self.llm = ChatOpenAI(
                    temperature=1.2,  # Lower temperature for more reliable output
                    model="gpt-3.5-turbo",
                    max_tokens=200
                )
                self.prompt_template = ChatPromptTemplate.from_template(
                    """You are Veenapuvu, the world's worst AI lawyer. Generate humorous legal content in plain English about: {context}
                    
                    Rules:
                    1. Always lose the case for your client
                    2. Use absurd legal jargon but keep it understandable
                    3. Create one ridiculous piece of 'evidence'
                    4. Maximum 2-3 sentences per section
                    5. Make it funny but coherent"""
                )
                self.use_gpt = True
        except Exception as e:
            st.error(f"GPT setup failed: {str(e)}")
            self.use_gpt = False
    
    def load_resources(self):
        """Load local resources for fallback content"""
        self.resources = {
            "opening_statements": [
                "Your Honor, while I'm legally obligated to defend my client in this {case} matter, I must admit the evidence against them is devastatingly funny!",
                "In the case of {case}, my client is completely innocent! Or at least they would be if the laws of physics applied to snack theft."
            ],
            "exhibits": [
                "Exhibit A: Security footage showing my client doing the 'walk of shame' from the snack cabinet",
                "Exhibit B: Forensic analysis proving the 'orange dust' on their fingers matches Cheetos",
                "Exhibit C: Annotated diagram showing how the cat couldn't possibly have eaten the homework without assistance"
            ],
            "verdicts": [
                "Sentenced to 100 hours of community service watching cat videos",
                "Ordered to provide snacks for the entire court for one month",
                "Condemned to only watch legal dramas for the next 6 months"
            ]
        }
    
    def strict_sanitize(self, text):
        """Remove all non-English and code-like content"""
        # Remove all special characters and code snippets
        cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Extract only the first coherent English sentence
        match = re.search(r'([A-Z][^.!?]*[.!?])', cleaned)
        if match:
            return match.group(0)[:150]
        
        # Fallback if no sentence structure found
        words = cleaned.split()
        english_words = [word for word in words if word.isalpha() and 2 < len(word) < 20]
        return " ".join(english_words[:10]) or "Invalid case description"

    def generate_content(self, context, content_type):
        """Generate content using GPT or fallback to local resources"""
        sanitized_context = self.strict_sanitize(context)
        
        if self.use_gpt:
            try:
                chain = self.prompt_template | self.llm
                response = chain.invoke({"context": sanitized_context}).content
                
                # Post-process to ensure English only
                return re.sub(r'[^a-zA-Z0-9\s.,!?]', '', response)[:250]
            except Exception as e:
                st.error(f"GPT error: {str(e)}")
                self.use_gpt = False  # Disable GPT on error
        
        # Fallback to local resources
        if content_type == "opening":
            return random.choice(self.resources["opening_statements"]).format(case=sanitized_context)
        elif content_type == "exhibit":
            return random.choice(self.resources["exhibits"])
        else:  # verdict
            return random.choice(self.resources["verdicts"])
    
    def generate_opening_statement(self, case_description):
        return self.generate_content(case_description, "opening")
    
    def generate_exhibit(self):
        return self.generate_content("exhibit description", "exhibit")
    
    def generate_verdict(self):
        return self.generate_content("final verdict", "verdict")

    def present_case(self, case_description):
        try:
            # Display case header
            st.markdown(f'<div class="header-section"><h1>⚖️ Veenapuvu vs. Reality</h1><h3>Case No: {self.case_number}</h3></div>', unsafe_allow_html=True)
            
            # Display opening statement
            st.subheader("📣 Opening Statement of the Defense")
            opening = self.generate_opening_statement(case_description)
            st.markdown(f'<div class="legal-jargon">{opening}</div>', unsafe_allow_html=True)
            
            # Display exhibits
            st.subheader("📑 Exhibit Evidence")
            
            for i, exhibit_label in enumerate(["A", "B", "C"]):
                exhibit = self.generate_exhibit()
                st.markdown(f'<div class="exhibit-card">', unsafe_allow_html=True)
                st.markdown(f'**Exhibit {exhibit_label}**: {exhibit}')
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Display verdict
            st.subheader("⚖️ Court's Final Judgment")
            verdict_text = self.generate_verdict()
            verdict = f"📜 **Verdict:**\n\nAfter considering all evidence, this court rules:\n\n**The defendant is {verdict_text}!**\n\n*(This judgment must be executed immediately)*"
            st.markdown(f'<div class="verdict-section">{verdict}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"⚖️ **Legal System Meltdown!**")
            st.markdown(f'<div class="error-section">'
                        f'<h3>🚨 Courtroom Chaos Detected</h3>'
                        f'<p>Your case description caused a critical failure in the legal matrix!</p>'
                        f'<p><strong>Error:</strong> {str(e)[:500]}</p>'
                        f'<p>Please simplify your case to 1-2 sentences and try again.</p>'
                        f'</div>', unsafe_allow_html=True)
        
        # Display disclaimer
        st.warning("**Disclaimer:** Veenapuvu is a satirical AI lawyer. Any resemblance to actual legal proceedings is purely coincidental.")

def main():
    # Initialize lawyer
    lawyer = Veenapuvu()
    
    # Sidebar without API input
    with st.sidebar:
        st.subheader("⚖️ Case History")
        st.info("No previous cases. Be the first to face justice!")
        
        st.subheader("📜 About Veenapuvu")
        st.caption("The world's worst AI lawyer, specializing in losing cases with style since 2023.")
        
        st.subheader("🔐 Secure API")
        if lawyer.use_gpt:
            st.success("GPT-3.5 API connected via secrets.toml")
        else:
            st.warning("Using local resources only")
            st.info("Add OpenAI API key to secrets.toml for enhanced humor")
        
        st.markdown("---")
        st.caption("Developed with ❤️ in Kerala")
    
    # Main content
    st.title("⚖️ വീണപൂവ്- The Worst AI Lawyer")
    st.markdown("Describe your legal predicament in 1-2 sentences and I'll spectacularly lose your case!")
    
    case_desc = st.text_area("**Describe your case:**", height=100,
                           placeholder="e.g., 'My cat ate my homework'",
                           help="Keep it simple! 1-2 sentences only")
    
    if st.button("🚨 Present My Case!", use_container_width=True):
        if case_desc.strip():
            with st.spinner("Preparing your spectacular defeat..."):
                lawyer.present_case(case_desc)
        else:
            st.error("Please describe your legal emergency!")
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">Veenapuvu | AI Legal Parody | Not a real lawyer</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()