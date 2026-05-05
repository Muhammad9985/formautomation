import random
from typing import Any

class PakistaniDataGenerator:
    FIRST_NAMES_MALE = [
        "Muhammad", "Ali", "Ahmed", "Hassan", "Usman", "Bilal", "Omar", "Farhan",
        "Saad", "Hamza", "Imran", "Shahid", "Tariq", "Kashif", "Naveed", "Salman",
        "Faisal", "Waqas", "Asad", "Saeed"
    ]
    FIRST_NAMES_FEMALE = [
        "Fatima", "Ayesha", "Zainab", "Maryam", "Amina", "Sana", "Hira", "Sadia",
        "Rabia", "Khadija", "Nadia", "Shehnaz", "Nasreen", "Saima", "Rubina", "Asma"
    ]
    LAST_NAMES = [
        "Khan", "Ahmed", "Siddiqui", "Sheikh", "Malik", "Butt", "Rana", "Javed",
        "Mirza", "Baig", "Hashmi", "Qureshi", "Ansari", "Farooqi", "Ismail", "Rizvi",
        "Naqvi", "Zafar", "Iqbal", "Shah"
    ]
    CITIES = [
        "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan",
        "Peshawar", "Quetta", "Hyderabad", "Sialkot", "Gujranwala", "Bahawalpur"
    ]
    STREET_SUFFIXES = ["Road", "Street", "Lane", "Avenue", "Block", "Sector", "Colony"]
    EDUCATION_LEVELS = ["Matric", "Intermediate", "Bachelor's", "Master's", "PhD", "Diploma"]
    GENDERS = ["Male", "Female", "Other"]
    SATISFACTION = ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
    YES_NO = ["Yes", "No"]
    AGREEMENT = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]

    @classmethod
    def generate_name(cls) -> str:
        gender = random.choice(["male", "female"])
        if gender == "male":
            first = random.choice(cls.FIRST_NAMES_MALE)
        else:
            first = random.choice(cls.FIRST_NAMES_FEMALE)
        last = random.choice(cls.LAST_NAMES)
        return f"{first} {last}"

    @classmethod
    def generate_phone(cls) -> str:
        prefix = random.choice(["300", "301", "302", "303", "304", "305", "306", "307", "308", "309",
                                "310", "311", "312", "313", "314", "315", "320", "321", "322", "323"])
        number = "".join(random.choices("0123456789", k=7))
        return f"+92 {prefix} {number[:3]} {number[3:]}"

    @classmethod
    def generate_email(cls, name: str) -> str:
        name_part = name.lower().replace(" ", ".")
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        return f"{name_part}@{random.choice(domains)}"

    @classmethod
    def generate_address(cls) -> str:
        house = random.randint(1, 999)
        street = f"{random.choice(cls.STREET_SUFFIXES)} {random.randint(1, 50)}"
        area = random.choice(["Gulshan", "Defence", "Model Town", "Gulberg", "Faisal Town", "Johar Town"])
        city = random.choice(cls.CITIES)
        return f"House {house}, {street}, {area}, {city}, Pakistan"

    @classmethod
    def generate_age(cls, min_age: int = 18, max_age: int = 65) -> int:
        return random.randint(min_age, max_age)

    @classmethod
    def generate_city(cls) -> str:
        return random.choice(cls.CITIES)

    @classmethod
    def generate_gender(cls) -> str:
        return random.choice(cls.GENDERS)

    @classmethod
    def generate_education(cls) -> str:
        return random.choice(cls.EDUCATION_LEVELS)

    @classmethod
    def generate_satisfaction(cls) -> str:
        return random.choice(cls.SATISFACTION)

    @classmethod
    def generate_yes_no(cls) -> str:
        return random.choice(cls.YES_NO)

    @classmethod
    def generate_agreement(cls) -> str:
        return random.choice(cls.AGREEMENT)

    @classmethod
    def generate_subjective_response(cls, topic: str = "") -> str:
        responses = [
            "I think this is a great initiative and I'm happy to participate.",
            "The service provided was satisfactory and met my expectations.",
            "I would recommend this to others based on my experience.",
            "There is room for improvement in certain areas.",
            "Overall a positive experience with some minor issues.",
            "I appreciate the effort put into this program.",
            "The process was smooth and well-organized.",
            "I found the information provided to be helpful and accurate."
        ]
        return random.choice(responses)

    @classmethod
    def generate_date(cls) -> str:
        year = random.randint(2000, 2026)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"

    MEDICAL_DEPARTMENTS = [
        "Cardiology", "Dermatology", "Emergency Medicine", "Family Medicine",
        "Gastroenterology", "General Surgery", "Internal Medicine", "Neurology",
        "Obstetrics and Gynecology", "Oncology", "Ophthalmology",
        "Orthopedics", "Pediatrics", "Psychiatry", "Radiology",
        "Urology", "Anesthesiology", "Pathology", "Pharmacy"
    ]

    IT_DEPARTMENTS = [
        "Software Development", "Web Development", "Data Science", "Machine Learning",
        "DevOps", "Cybersecurity", "Network Administration", "Database Administration",
        "IT Support", "Quality Assurance", "UI/UX Design", "Product Management",
        "Cloud Computing", "Artificial Intelligence", "Mobile Development"
    ]

    BUSINESS_DEPARTMENTS = [
        "Marketing", "Sales", "Human Resources", "Finance", "Accounting",
        "Operations", "Customer Service", "Business Development",
        "Supply Chain", "Procurement", "Legal", "Administration"
    ]

    @classmethod
    def generate_department(cls, label: str = "") -> str:
        label_lower = label.lower()
        if any(word in label_lower for word in ["medical", "health", "hospital", "doctor", "patient", "clinic"]):
            return random.choice(cls.MEDICAL_DEPARTMENTS)
        if any(word in label_lower for word in ["it", "tech", "software", "computer", "programming", "engineer"]):
            return random.choice(cls.IT_DEPARTMENTS)
        if any(word in label_lower for word in ["business", "corporate", "company", "office", "finance"]):
            return random.choice(cls.BUSINESS_DEPARTMENTS)
        # Return random department from all
        all_depts = cls.MEDICAL_DEPARTMENTS + cls.IT_DEPARTMENTS + cls.BUSINESS_DEPARTMENTS
        return random.choice(all_depts)

    NURSE_SPECIALTIES = [
        "Emergency Room Nurse", "ICU Nurse", "Pediatric Nurse", "Operating Room Nurse",
        "Labor and Delivery Nurse", "Oncology Nurse", "Psychiatric Nurse",
        "Cardiac Nurse", "Neonatal Intensive Care Nurse", "Orthopedic Nurse",
        "Surgical Nurse", "Medical-Surgical Nurse", "Community Health Nurse",
        "Nurse Practitioner", "Clinical Nurse Specialist", "Nurse Anesthetist",
        "Public Health Nurse", "School Nurse", "Home Health Nurse"
    ]

    NURSE_DEGREES = [
        "Diploma in Nursing", "Associate Degree in Nursing (ADN)",
        "Bachelor of Science in Nursing (BSN)", "Master of Science in Nursing (MSN)",
        "Doctor of Nursing Practice (DNP)", "PhD in Nursing"
    ]

    SHIFT_TIMINGS = [
        "Morning Shift (6AM-2PM)", "Day Shift (8AM-4PM)", "Evening Shift (4PM-12AM)",
        "Night Shift (12AM-8AM)", "Rotating Shifts"
    ]

    EXPERIENCE_LEVELS = [
        "Less than 1 year", "1-2 years", "3-5 years",
        "5-10 years", "More than 10 years"
    ]

    SATISFACTION_SCORES = [
        "Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"
    ]

    YES_NO = ["Yes", "No"]

    AGREEMENT = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]

    @classmethod
    def generate_nurse_data(cls, submission_id: int, total_submissions: int = 300) -> dict:
        """Generate complete nurse data set for contextual form filling.
        Generates unique data based on submission_id to ensure 300 unique submissions.
        """
        # Use submission_id to generate unique but deterministic data
        random.seed(submission_id * 12345)  # Unique seed per submission

        # Generate unique name
        gender = "male" if submission_id % 3 == 0 else "female"  # ~33% male, 67% female
        if gender == "male":
            first = cls.FIRST_NAMES_MALE[(submission_id - 1) % len(cls.FIRST_NAMES_MALE)]
        else:
            first = cls.FIRST_NAMES_FEMALE[(submission_id - 1) % len(cls.FIRST_NAMES_FEMALE)]
        last = cls.LAST_NAMES[(submission_id - 1) % len(cls.LAST_NAMES)]
        full_name = f"{first} {last}"

        # Generate basic info with variations
        base_age = 22 + (submission_id % 38)  # Ages 22-59
        age = str(base_age)

        # Generate phone with unique last digits
        prefix = cls.generate_phone().split()[-1].split("-")[0]  # Get network prefix
        unique_digits = f"{(submission_id % 1000):03d}{(submission_id % 100):02d}"  # Unique last 5 digits
        phone = f"+92 {prefix} {unique_digits[:3]} {unique_digits[3:]}"

        # Generate email
        email_name = full_name.lower().replace(" ", ".")
        email = f"{email_name}{submission_id}@gmail.com"

        # Generate address with variation
        house = (submission_id % 999) + 1
        street = f"{random.choice(cls.STREET_SUFFIXES)} {random.randint(1, 50)}"
        area = random.choice(["Gulshan", "Defence", "Model Town", "Gulberg", "Faisal Town", "Johar Town"])
        city = cls.CITIES[(submission_id - 1) % len(cls.CITIES)]
        address = f"House {house}, {street}, {area}, {city}, Pakistan"

        # Education and experience based on age
        if base_age < 25:
            education = cls.NURSE_DEGREES[0]  # Diploma
        elif base_age < 30:
            education = cls.NURSE_DEGREES[1]  # ADN
        elif base_age < 40:
            education = random.choice(cls.NURSE_DEGREES[2:4])  # BSN or MSN
        else:
            education = random.choice(cls.NURSE_DEGREES[3:])  # MSN, DNP, or PhD

        # Specialty based on experience
        specialty = cls.NURSE_SPECIALTIES[(submission_id - 1) % len(cls.NURSE_SPECIALTIES)]
        department = cls.MEDICAL_DEPARTMENTS[(submission_id - 1) % len(cls.MEDICAL_DEPARTMENTS)]

        # Experience based on age
        if base_age < 25:
            experience = cls.EXPERIENCE_LEVELS[0]  # <1 year
        elif base_age < 30:
            experience = cls.EXPERIENCE_LEVELS[1]  # 1-2 years
        elif base_age < 40:
            experience = cls.EXPERIENCE_LEVELS[2]  # 3-5 years
        elif base_age < 50:
            experience = cls.EXPERIENCE_LEVELS[3]  # 5-10 years
        else:
            experience = cls.EXPERIENCE_LEVELS[4]  # >10 years

        shift = cls.SHIFT_TIMINGS[(submission_id - 1) % len(cls.SHIFT_TIMINGS)]

        # Reset random seed to avoid affecting other parts
        random.seed()

        return {
            "name": full_name,
            "first_name": first,
            "last_name": last,
            "age": age,
            "phone": phone,
            "email": email,
            "address": address,
            "city": city,
            "gender": "Male" if gender == "male" else "Female",
            "education": education,
            "specialty": specialty,
            "department": department,
            "experience": experience,
            "shift": shift,
            "satisfaction": cls.SATISFACTION_SCORES[(submission_id - 1) % len(cls.SATISFACTION_SCORES)],
            "agreement": cls.AGREEMENT[(submission_id - 1) % len(cls.AGREEMENT)],
            "yes_no": cls.YES_NO[(submission_id - 1) % 2],
            "subjective": cls.generate_subjective_response("nurse experience"),
            "date": cls.generate_date()
        }

    @classmethod
    def context_aware_value(cls, label: str, field_type: str = "text", nurse_data: dict | None = None, submission_id: int = 0) -> Any:
        """Generate context-aware value based on field label analysis.
        If nurse_data is provided, use it for contextual answers.
        """
        if not label or label == "Unknown Field":
            # Fallback based on field type
            if field_type == "text":
                return cls.generate_subjective_response("")
            return ""

        label_lower = label.lower()

        # Use pre-generated nurse data if available
        if nurse_data:
            if any(word in label_lower for word in ["name", "full name", "your name"]):
                return nurse_data.get("name", cls.generate_name())
            if "first name" in label_lower:
                return nurse_data.get("first_name", "")
            if "last name" in label_lower:
                return nurse_data.get("last_name", "")
            if any(word in label_lower for word in ["phone", "mobile", "contact", "cell", "whatsapp"]):
                return nurse_data.get("phone", cls.generate_phone())
            if any(word in label_lower for word in ["email", "e-mail", "mail"]):
                return nurse_data.get("email", cls.generate_email(nurse_data.get("name", "")))
            if any(word in label_lower for word in ["address", "location", "residence"]):
                return nurse_data.get("address", cls.generate_address())
            if any(word in label_lower for word in ["age", "years old"]):
                if "date" in label_lower or "dob" in label_lower or "birth" in label_lower:
                    return nurse_data.get("date", cls.generate_date())
                return nurse_data.get("age", str(cls.generate_age()))
            if any(word in label_lower for word in ["city", "town"]):
                return nurse_data.get("city", cls.generate_city())
            if any(word in label_lower for word in ["gender", "sex"]):
                return nurse_data.get("gender", cls.generate_gender())
            if any(word in label_lower for word in ["education", "qualification", "degree"]):
                return nurse_data.get("education", cls.generate_education())
            if any(word in label_lower for word in ["specialty", "specialization"]):
                return nurse_data.get("specialty", "")
            if any(word in label_lower for word in ["department", "dept", "which department"]):
                return nurse_data.get("department", cls.generate_department(label))
            if any(word in label_lower for word in ["experience", "years of experience"]):
                return nurse_data.get("experience", "")
            if any(word in label_lower for word in ["shift", "timing", "schedule"]):
                return nurse_data.get("shift", "")
            if any(word in label_lower for word in ["satisfaction", "rating", "rate", "happy"]):
                return nurse_data.get("satisfaction", cls.generate_satisfaction())
            if any(word in label_lower for word in ["agree", "opinion", "disagree"]):
                return nurse_data.get("agreement", cls.generate_agreement())
            if any(word in label_lower for word in ["yes", "no", "do you"]):
                return nurse_data.get("yes_no", cls.generate_yes_no())
            if any(word in label_lower for word in ["comment", "feedback", "suggestion", "review"]):
                return nurse_data.get("subjective", cls.generate_subjective_response("nurse experience"))
            if any(word in label_lower for word in ["date", "when", "dob", "birth"]):
                return nurse_data.get("date", cls.generate_date())

        # Fallback to generated data if nurse_data doesn't have the field
        # (rest of original logic...)
        if any(word in label_lower for word in ["department", "dept", "which department"]):
            return cls.generate_department(label)
        if any(word in label_lower for word in ["name", "full name", "your name"]):
            return cls.generate_name()
        if any(word in label_lower for word in ["phone", "mobile", "contact"]):
            return cls.generate_phone()
        if any(word in label_lower for word in ["email", "e-mail"]):
            return cls.generate_email(cls.generate_name())
        if any(word in label_lower for word in ["address", "location"]):
            return cls.generate_address()
        if "age" in label_lower or "years old" in label_lower:
            return str(cls.generate_age())
        if "city" in label_lower or "town" in label_lower:
            return cls.generate_city()
        if "gender" in label_lower:
            return cls.generate_gender()
        if "education" in label_lower:
            return cls.generate_education()
        if "satisfaction" in label_lower:
            return cls.generate_satisfaction()
        if "agree" in label_lower:
            return cls.generate_agreement()
        if "yes" in label_lower or "no" in label_lower:
            return cls.generate_yes_no()
        if "date" in label_lower:
            return cls.generate_date()

        # Text field fallbacks
        if field_type == "text":
            return cls.generate_subjective_response(label)

        return ""
