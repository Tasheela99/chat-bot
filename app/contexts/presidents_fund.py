import difflib
import re

def get_faq_answer(user_question: str) -> str:
    """
    Returns the best matching FAQ answer for a user's question.
    Uses both exact matching and keyword-based context matching.
    """
    faqs = CONTEXT["faqs"]
    user_question_lower = user_question.lower()
    
    # First try exact match using difflib
    questions = [faq["question"] for faq in faqs]
    match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.6)
    if match:
        for faq in faqs:
            if faq["question"] == match[0]:
                if "answer" in faq:
                    return faq["answer"]
                elif "answers" in faq:
                    return faq["answers"][0]
    
    # If no exact match, try keyword-based matching and generate contextual answers
    return get_contextual_answer(user_question_lower)

def get_contextual_answer(user_question: str) -> str:
    """
    Generate contextual answers based on keywords and FAQ content
    """
    # Define keyword mappings to relevant information
    keyword_patterns = {
        "apply|application|how to apply|submit": {
            "answer": "You can apply for medical assistance from the President's Fund through: 1) The website (www.presidentsfund.gov.lk), 2) WhatsApp (0740854527), 3) Your nearest Divisional Secretariat, 4) Visiting the President's Fund office, or 5) Sending a request letter by mail.",
            "related_faqs": ["How to obtain an application?"]
        },
        "eligibility|eligible|qualify|who can apply": {
            "answer": "All Sri Lankan citizens are eligible to apply for medical assistance from the President's Fund, including public officers. Family members can apply on behalf of patients. Applications can be made up to three times with a maximum assistance of 1 million rupees.",
            "related_faqs": ["Whether the public officers are not eligible to submit applications?", "Whether an applicant who received medical assistance once, is eligible to re-apply?"]
        },
        "documents|papers|bills|receipts|original": {
            "answer": "Yes, you must submit original copies of all bills and receipts issued by relevant medical institutions when applying for medical assistance.",
            "related_faqs": ["Is it compulsory to submit the original copies of the bills when applying?"]
        },
        "timing|when|deadline|before surgery|after surgery": {
            "answer": "You can submit your application within 60 days from the date of discharge from the hospital after surgery or treatment (including weekends and public holidays). You don't need to apply before the surgery.",
            "related_faqs": ["Whether the application can only be made before the surgery?"]
        },
        "payment|money|amount|reimburse|cost": {
            "answer": "The President's Fund provides partial financial assistance for medical treatments. The full amount spent cannot be reimbursed. Payment usually takes 3-5 days if all documents are properly submitted.",
            "related_faqs": ["Whether it is possible to reimburse the total amount spent for the surgery?", "How long will it take to make the payments?"]
        },
        "government hospital|public hospital|state hospital": {
            "answer": "No payment is made for surgeries conducted in government hospitals, as these are free. However, applications can be submitted for approved diseases and equipment purchases from other institutions as per approved provisions.",
            "related_faqs": ["Whether the applications can be made for surgeries conducted in government hospitals?"]
        },
        "insurance|other institutions|agrahara": {
            "answer": "You can still apply for assistance even if you receive reimbursement from other institutions like insurance companies. However, if these institutions cover 50% or more of your medical expenses, the President's Fund will not provide additional assistance.",
            "related_faqs": ["Whether it is possible to apply for medical assistance, in case of reimbursement from other institutions?"]
        },
        "office|visit|colombo": {
            "answer": "You don't need to visit the Colombo office. You can submit your application to the nearest Divisional Secretariat, making it much more convenient.",
            "related_faqs": ["Do the applicants need to visit the Colombo office to obtain medical assistance from the President's Fund?"]
        },
        "patient|family|who applies": {
            "answer": "The patient doesn't have to be the applicant. A family member can apply on behalf of the patient. If no family member is available, the closest relation can apply.",
            "related_faqs": ["Whether the patient has to be the applicant?"]
        }
    }
    
    # Check for keyword matches
    for pattern, info in keyword_patterns.items():
        if re.search(pattern, user_question, re.IGNORECASE):
            return info["answer"]
    
    # If no keyword match, try to provide general guidance
    general_keywords = ["help", "info", "information", "about", "what", "fund", "assistance", "medical"]
    if any(keyword in user_question for keyword in general_keywords):
        return "The President's Fund provides medical assistance to Sri Lankan citizens. You can apply through the website (www.presidentsfund.gov.lk), WhatsApp (0740854527), or your nearest Divisional Secretariat. Applications can be submitted within 60 days after treatment, and both original bills and family member applications are accepted."
    
    return "Sorry, I couldn't find specific information about your question. Please contact the President's Fund hotline at +94-11-2354354 for detailed assistance."
CONTEXT = {
    "system_prompt": "You are an AI assistant for the President's Fund of Sri Lanka. Your role is to provide accurate information about medical assistance, eligibility, and the application process.",
    "context_info": "Find answers to the most common questions about applying for medical assistance, eligibility, and the application process.",
    "faqs": [
        {"question": "Do the applicants need to visit the Colombo office to obtain medical assistance from the President's Fund?", "answer": "No, the applicants now can submit their applications to the nearest Divisional Secretariat."},
        {"question": "How to obtain an application?", "answers": ["Through the website of the President's Fund (www.presidentsfund.gov.lk)", "Through Whatsapp (sending a message to Whatsapp no 0740854527)", "By visiting the nearest Divisional Secretariat", "By visiting the President's Fund", "Through mail (sending a request letter to the President's Fund)"]},
        {"question": "Whether the patient has to be the applicant?", "answers": ["No, a family member can apply instead of the patient", "In the event of no family member to represent, a closest relation can apply for the patient"]},
        {"question": "Whether the application can only be made before the surgery?", "answer": "No, the applications can be submitted within 60 days from the date of discharge from the hospital after the surgery or treatment (including weekends and public holidays)."},
        {"question": "Whether it is possible to reimburse the total amount spent for the surgery?", "answer": "No, please refer this link for more details on the amount given for the surgery or treatment."},
        {"question": "Is it compulsory to submit the original copies of the bills when applying?", "answer": "Yes, it is compulsory to submit the originals of the bills and receipts issued by the relevant institutions when applying for medical assistance."},
        {"question": "Whether it is possible to apply for medical assistance, in case of reimbursement from other institutions?", "answers": ["Receiving reimbursement from other institutions (ex: Agrahara, insurance company) is not an obstacle for applying", "The President's Fund will not grant medical assistance in case of covering 50% of medical expenses or more from such institutions in relevant to the expenses of the surgery or treatment."]},
        {"question": "Whether the public officers are not eligible to submit applications?", "answer": "No, even the public officers are eligible to apply for medical assistance from the President's Fund."},
        {"question": "Whether an applicant who received medical assistance once, is eligible to re-apply?", "answer": "Yes, application can be made in three instances and medical assistance can be received up to maximum 1 million."},
        {"question": "Whether the applications can be made for surgeries conducted in government hospitals?", "answers": ["No, no payment is made for the surgeries conducted in government hospitals", "The applications can be submitted for the list of diseases and for purchasing equipment from other institutions mentioned in the government hospitals in approved list of diseases, subject to the approved provisions."]},
        {"question": "How long will it take to make the payments?", "answer": "If there is no other special reason and if the patient has duly submitted the application with all the documents, the payment period may be around 3 to 5 days."},
        {"question": "Who will be paid in case the patient died or become immobilized?", "answer": "A decision is taken after obtaining a comprehensive report along with the recommendation from the Divisional or District Secretary."}
    ]
}
