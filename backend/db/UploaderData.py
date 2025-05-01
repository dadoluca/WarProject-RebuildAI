from db.VectorDBManager import VectorDBManager  
from dotenv import load_dotenv
import os


load_dotenv()

class UploaderData:
    
    def __init__(self):
        pinecone_api = os.getenv("PINECONE_API_KEY")
        openai_api = os.getenv("OPENAI_API_KEY")
        
        if not pinecone_api or not openai_api:
            raise ValueError("Missing required API keys in environment variables")
        
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "war-use-cases")
        
        self.use_cases_db = VectorDBManager(
            pinecone_api=pinecone_api,
            openai_api=openai_api,
            index_name=self.index_name,
            namespace="use_cases"
        )
        
        self.risks_db = VectorDBManager(
            pinecone_api=pinecone_api,
            openai_api=openai_api,
            index_name=self.index_name,
            namespace="risks"
        )
        
        self.mitigations_db = VectorDBManager(
            pinecone_api=pinecone_api,
            openai_api=openai_api,
            index_name=self.index_name,
            namespace="mitigations"
        )
        
        
        self.benefits_db = VectorDBManager(
            pinecone_api=pinecone_api,
            openai_api=openai_api,
            index_name=self.index_name,
            namespace="benefits"
        )
        
    def populate_use_cases_data(self, data):
        self.use_cases_db.add_data(data)
    
    def populate_risks_data(self, data):
        self.risks_db.add_data(data)
    
    def populate_mitigations_data(self, data):
        self.mitigations_db.add_data(data)
    
    def populate_benefits_data(self, data):
        self.benefits_db.add_data(data)
    
    def populate_sample_data(self):
        """Populate the database with sample data for testing"""
        
        # Sample use cases data
        use_cases = [
            {
                "to_embedd": "AI in humanitarian assistance during war, including chatbots for psychological support and route planning for aid delivery",
                "metadata": {
                    "id": "uc1",
                    "title": "AI Chatbots for Psychological Support",
                    "description": "Using AI-powered chatbots to provide basic psychological support to war victims who have limited access to mental health professionals.",
                    "context": "Post-conflict zones with damaged infrastructure and limited humanitarian workers"
                }
            },
            {
                "to_embedd": "AI for conflict prediction and prevention using satellite imagery and social media monitoring",
                "metadata": {
                    "id": "uc2",
                    "title": "AI-Based Conflict Early Warning System",
                    "description": "Using machine learning algorithms to analyze satellite imagery, social media patterns, and other data sources to predict potential conflict escalation.",
                    "context": "Pre-conflict or ongoing conflict zones where early intervention could prevent escalation"
                }
            },
            {
                "to_embedd": "AI for detecting unexploded ordnance using drone imagery and computer vision",
                "metadata": {
                    "id": "uc3",
                    "title": "AI-Powered UXO Detection",
                    "description": "Using computer vision and machine learning with drone imagery to detect and map unexploded ordnance (UXO) in post-conflict areas.",
                    "context": "Post-conflict areas with potential landmines and unexploded bombs"
                }
            },
            {
                "to_embedd": "AI for facial recognition to reunite displaced families in refugee camps",
                "metadata": {
                    "id": "uc4",
                    "title": "Facial Recognition for Family Reunification",
                    "description": "Using facial recognition technology to help reunite family members separated during conflict and displacement.",
                    "context": "Refugee camps and displacement centers"
                }
            }
        ]
        
        # Sample risks and benefits data
        risks = [
            {
                "to_embedd": "risks and benefits of AI Chatbots for Psychological Support in war zones",
                "metadata": {
                    "id": "rb1",
                    "risks": "Privacy concerns with sensitive personal data; Inadequate support for severe trauma cases; Overreliance on AI instead of human therapists",
                    "benefits": "24/7 availability; Scalability to reach more victims; No language barriers with multilingual models; Reduced stigma compared to in-person therapy"
                }
            },
            {
                "to_embedd": "risks and benefits of AI-Based Conflict Early Warning System in conflict zones",
                "metadata": {
                    "id": "rb2",
                    "risks": "False alarms causing unnecessary panic; Ethical issues with surveillance; Dependency on technology for critical decisions",
                    "benefits": "Early intervention opportunities; Data-driven policy decisions; Reduced human bias in conflict assessment"
                }
            },
            {
                "to_embedd": "risks and benefits of AI-Powered UXO Detection in post-conflict areas",
                "metadata": {
                    "id": "rb3",
                    "risks": "False negatives leaving dangerous areas unmarked; Technical limitations in difficult terrain; High implementation costs",
                    "benefits": "Faster clearance of contaminated areas; Reduced risk to human deminers; More efficient resource allocation"
                }
            },
            {
                "to_embedd": "risks and benefits of Facial Recognition for Family Reunification in refugee contexts",
                "metadata": {
                    "id": "rb4",
                    "risks": "Privacy and consent issues; Potential misuse of collected biometric data; Algorithmic bias affecting certain ethnic groups",
                    "benefits": "Speed of family reunification; Scale of operations possible; Reduced administrative burden"
                }
            }
        ]
        
        # Sample mitigations data
        mitigations = [
            {
                "to_embedd": "mitigations for Privacy concerns with sensitive personal data in AI Chatbots",
                "metadata": {
                    "id": "m1",
                    "mitigations": "Implement end-to-end encryption; Establish clear data retention policies; Use anonymization techniques; Obtain informed consent; Regular security audits"
                }
            },
            {
                "to_embedd": "mitigations for Inadequate support for severe trauma cases in AI mental health support",
                "metadata": {
                    "id": "m2",
                    "mitigations": "Implement robust triage system to escalate severe cases to human professionals; Clear disclosure of AI limitations; Integration with existing mental health services"
                }
            },
            {
                "to_embedd": "mitigations for False alarms in conflict prediction systems",
                "metadata": {
                    "id": "m3",
                    "mitigations": "Implement multi-factor verification protocols; Human-in-the-loop review process; Continuous model retraining with feedback; Transparency about confidence levels"
                }
            },
            {
                "to_embedd": "mitigations for Algorithmic bias in facial recognition systems",
                "metadata": {
                    "id": "m4",
                    "mitigations": "Diverse training data from all represented populations; Regular bias audits; Alternative identification methods available; Explainable AI approaches"
                }
            }
        ]
        
        benefits = []
        
        # Add data to respective namespaces
        if use_cases:
            print("Populating use cases database...")
            self.populate_use_cases_data(use_cases)
        
        if risks:
            print("Populating risks and benefits database...")
            self.populate_risks_data(risks)
        
        if mitigations:
            print("Populating mitigations database...")
            self.populate_mitigations_data(mitigations)
        
        if benefits:
            print("Populating benefits database...")
            self.populate_benefits_data(benefits)
        
        print("Sample data population complete")

    
    def delete_all_data(self):
        """
        Deletes all data from the Pinecone knowledge base.
        """
        print("Deleting all data from the Pinecone knowledge base...")
        self.use_cases_db.delete_all_chunks()
        self.risks_db.delete_all_chunks()
        self.mitigations_db.delete_all_chunks()
        self.benefits_db.delete_all_chunks()
        print("All data deleted successfully.")