#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration module for the Values Report Bot
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    """Configuration class for the bot"""
    
    # Telegram Bot API Token
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # Webhook settings (for production)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)
    
    # Supabase configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # PDF Generation settings
    PDF_FONT = "Poppins"
    PDF_PRIMARY_COLOR = "#333333"  # Dark grey
    PDF_SECONDARY_COLOR = "#FFFFFF"  # White
    
    # Values data - All 65 predetermined values
    VALUES_LIST = [
	{"value": "Fun", "description": "Prioritising enjoyment, playfulness, and lightheartedness in one's life.", "schwartz_category": "Hedonism", "gouveia_category": "Excitement"},
	{"value": "Happiness", "description": "Prioritising well-being, meaningful relationships, fulfilment, and a purposeful, joyful life.", "schwartz_category": "Hedonism", "gouveia_category": "Excitement"},
	{"value": "Humour", "description": "Enriching life with positivity, laughter, and creativity through amusement and joy.", "schwartz_category": "Hedonism", "gouveia_category": "Excitement"},
	{"value": "Challenge", "description": "Pushing one's limits and boundaries, appreciating the process of striving beyond one's current capabilities.", "schwartz_category": "Stimulation", "gouveia_category": "Excitement"},
	{"value": "Intelligence", "description": "Appreciating knowledge and critical thinking, admiring learning, problem-solving, and intellectual growth.", "schwartz_category": "Stimulation", "gouveia_category": "Excitement"},
	{"value": "Balance", "description": "Maintaining equilibrium across different aspects of one's life. Striving for a well-rounded life with coexisting components.", "schwartz_category": "Security", "gouveia_category": "Existence"},
	{"value": "Financial Security", "description": "Prioritising the peace of mind and stability that comes from meeting one's own defined needs.", "schwartz_category": "Security", "gouveia_category": "Existence"},
	{"value": "Health; Physical Wellbeing", "description": "Prioritising self-care and holistic well-being by taking conscious actions to maintain physical and mental fitness.", "schwartz_category": "Security", "gouveia_category": "Existence"},
	{"value": "Resilience", "description": "Persevering through setbacks healthily through reflection, recuperation, and recalibration. Bouncing back from failures.", "schwartz_category": "Security", "gouveia_category": "Existence"},
	{"value": "Security", "description": "Prioritising stability and safety for one's overall wellbeing.", "schwartz_category": "Security", "gouveia_category": "Existence"},
	{"value": "Care", "description": "Prioritising the wellbeing of others, showing compassion, understanding, and genuine concern for their needs.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Dependability", "description": "Prioritising reliability, consistency, and trustworthiness in oneself and others.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Empathy", "description": "Understanding others' perspectives and feelings through emotional connection and a common humanity.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Family", "description": "Nurturing and cherishing relationships with family members, actively investing time and effort into a family unit.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Friendships; Relationships", "description": "Forging supportive and fulfilling relationships with others outside of one's immediate family for belonging and happiness.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Generosity", "description": "Promoting selflessness and giving to foster empathy and interconnectedness between persons.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Love; Affection", "description": "Placing great importance on emotional connection with others; having meaningful relationships that bring joy and emotional fulfilment.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "People; Community", "description": "Creating lasting change through collective action and shared experiences. Fostering a sense of belonging.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Service", "description": "Dedicating one's time, energy, and resources to help others in need in order to make a positive difference.", "schwartz_category": "Benevolence", "gouveia_category": "Interactive"},
	{"value": "Discipline", "description": "Respecting self-control and an adherence to rules and/or structure. Appreciating the importance of being organised.", "schwartz_category": "Conformity", "gouveia_category": "Normative"},
	{"value": "Honesty; Trustworthiness", "description": "Exhibiting transparency by openly sharing thoughts and opinions to cultivate trust, reliability, and mutual respect.", "schwartz_category": "Conformity", "gouveia_category": "Normative"},
	{"value": "Morality", "description": "Considering ethical implications, striving to uphold fairness, compassion, honesty, and integrity in actions.", "schwartz_category": "Conformity", "gouveia_category": "Normative"},
	{"value": "Patience", "description": "Respecting steady progress and the importance of resolute biding of time to achieve an outcome without immediacy.", "schwartz_category": "Conformity", "gouveia_category": "Normative"},
	{"value": "Responsibility", "description": "Prioritising accountability and reliability by consistently fulfilling one's commitments to oneself or others.", "schwartz_category": "Conformity", "gouveia_category": "Normative"},
	{"value": "Integrity; Righteousness", "description": "Practising honesty and authenticity, maintaining wholeness and moral uprightness in one's words and actions.", "schwartz_category": "Tradition", "gouveia_category": "Normative"},
	{"value": "Loyalty", "description": "Priorisiting commitment, trust, and faithfulness, and giving unwavering support to a person, group, or cause.", "schwartz_category": "Tradition", "gouveia_category": "Normative"},
	{"value": "Spirituality; Faith", "description": "Connecting and believing in a higher power than oneself or the interconnectedness of all life, sacred meanings, and peace.", "schwartz_category": "Tradition", "gouveia_category": "Normative"},
	{"value": "Tradition", "description": "Appreciating long-established customs and practices that serve as a cornerstone for cultural identity and history.", "schwartz_category": "Tradition", "gouveia_category": "Normative"},
	{"value": "Authority", "description": "Having a high regard for mandated and/or official leadership. Respecting organisational or hierarchical structures.", "schwartz_category": "Power", "gouveia_category": "Promotion"},
	{"value": "Influence", "description": "Seeking to shape opinions and decisions through effective communication and interpersonal skills.", "schwartz_category": "Power", "gouveia_category": "Promotion"},
	{"value": "Power", "description": "Desiring control and/or influence to attain prominence or dominance in a given aspect of one's life.", "schwartz_category": "Power", "gouveia_category": "Promotion"},
	{"value": "Prosperity; Wealth", "description": "Prioritising financial success; striving to achieve financial stability and/or abundance.", "schwartz_category": "Power", "gouveia_category": "Promotion"},
	{"value": "Accountability", "description": "Accepting responsibility for mistakes, upholding high standards and grounding one's work in evidence.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Achievement; Success", "description": "Recognising and appreciating accomplishments. Outcome-driven.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Competence; Efficacy", "description": "Acquiring and demonstrating knowledge, skills, and expertise with a belief in one's abilities to achieve.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Competition", "description": "Being motivated by comparing skills and progress with others in the pursuit to surpass them.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Grit", "description": "Commiting to persevere and overcome obstacles; resilience to achieve long-term success.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Mastery", "description": "Developing expertise by seeking improvement and excellence through disciplined practice and skill refinement.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Pragmatism", "description": "Focusing on realistic improvements, incremental change and inspiring collaboration to foster progress across multiple paths.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Recognition", "description": "Appreciating validation or praise for one's efforts, achievements, or contributions.", "schwartz_category": "Achievement", "gouveia_category": "Promotion"},
	{"value": "Autonomy", "description": "Valuing the power to make one's own decisions, with an emphasis on self-governance and personal choice.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Courage", "description": "Challenging the status quo, speaking truth to power, understanding one's relationships with nature, community, and ancestors to act with inner resolve.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Creativity", "description": "Appreciating the ability to generate new ideas, be expressive, and create.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Curiosity", "description": "Having the desire to explore, learn, and understand the world, creating richer engagement with life experiences.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Flexibility", "description": "Appreciating the ability to adapt to changes, have autonomy over one's circumstances, and the fluidity of adjustment.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Fortitude", "description": "Admiring the quality of mental and emotional strength, appreciating inner resilience and determination.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Freedom", "description": "Not being limited by boundaries. Having the liberty to make decisions however one wishes.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Growth", "description": "Developing oneself and pursuing lifelong learning, making progress instead of maintaining a status quo.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Imagination", "description": "Envisioning a just world and bringing innovative ideas, new questions, and storytelling to address challenges.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Independence", "description": "Prioritising self-reliance and autonomy to control your actions and destiny without relying on others.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Purpose", "description": "Being motivated by a higher calling, or a deeply held aspiration rooted in intrinsic values and/or upbringing.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Simplicity", "description": "Appreciating a minimalistic and no-frills approach to life, work, and living. Minimising excess.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Wisdom", "description": "Appreciating established knowledge, experience, and the judicious application of those to make sound decisions.", "schwartz_category": "Self-Direction", "gouveia_category": "Suprapersonal"},
	{"value": "Beauty", "description": "Valuing the appearance of something; prioritising the aesthetics.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Diversity", "description": "Actively recognising and respecting the differences among people. Celebrating the value and uniqueness of each person.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Equality", "description": "Advocating for a society where everyone is treated with the same level of fairness, respect, and equal opportunity.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Harmony", "description": "Prioritising peace, balance, and unity to foster understanding and cooperation in your life and relationships.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Hope", "description": "Confidently believing in a better future; inspiring perseverance even in difficult moments for a higher purpose.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Inclusivity", "description": "Fostering a sense of genuine welcomeness and belonging; Bridging divides and finding common ground amongst diversity.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Interconnectedness", "description": "Recognising the intricate connections between people, communities, and ecosystems.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Peace", "description": "Prioritising harmony and cooperation to create safe, tranquil environments free from conflict and violence.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Respect", "description": "Treating others with dignity, empathy, and consideration. Fostering positive relationships built on mutual understanding.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Stewardship", "description": "Taking responsibility for managing resources effectively and ethically, being thoughtful and conscientious for the future.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Sustainability", "description": "Prioritising practices that ensure long-term health, focusing on renewing and reducing to support the environment and society.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
	{"value": "Teamwork; Collaboration", "description": "Working together toward a common goal, leveraging diverse skills, perspectives, and strengths to achieve better outcomes.", "schwartz_category": "Universalism", "gouveia_category": "Suprapersonal"},
    ]
    
    # Report sections with corresponding prompts
    REPORT_SECTIONS = [
        {
            "title": "What does this mean for me?",
            "question": "What does this mean for me?",
            "description": "Personal analysis of values",
            "prompt_template": """
I would like you to consider the following information as act as a life coach to me. I am currently aged {age} and based in {country}, with my occupation being {occupation}. I just did an exercise to determine what my top values are. My top five values in ranked order from 1st to 5th are {value1}, {value2}, {value3}, {value4}, and {value5}. My subsequent five values in no particular ranked order are {value6}, {value7}, {value8}, {value9}, and {value10}.

These values have the following descriptors:
- {value1}: {desc1}
- {value2}: {desc2}
- {value3}: {desc3}
- {value4}: {desc4}
- {value5}: {desc5}
- {value6}: {desc6}
- {value7}: {desc7}
- {value8}: {desc8}
- {value9}: {desc9}
- {value10}: {desc10}

Noting the ranked order of my top 5 values and the subsequent 5 values which also hold importance to me, and also all the information you have about me, I want you to prepare an encouraging and uplifting analysis of who I am as can be observed from my values and presented to me as if you are writing a personalised personality diagnostic report.

Your response should be formal yet uplifting. This is considered a personality diagnostic report and should only contain body text of no more than 300 words. Hold your response to a high degree of relevance. Noting all of the information you are given about me and my values, this response should be to directly answer the question: What does this mean for me?
"""
        },
        {
            "title": "Are my values in parallel or in tension?",
            "question": "Are my values in parallel or in tension?",
            "description": "Analysis of value alignment and conflicts",
            "prompt_template": """
I would like you to reference the 1992 research on Basic Human Values by Shalom Schwartz and any subsequent studies done with him or based heavily on his work. Ensure that your response to me is based solely on the peer-reviewed and credible research done on this topic. 
My top five values in ranked order from 1st to 5th are {value1}, {value2}, {value3}, {value4}, and {value5}. My subsequent five values in no particular ranked order are {value6}, {value7}, {value8}, {value9}, and {value10}.

I have determined that they correspond very closely to the following Basic Human Values according to Schwartz:
- {value1}: {schwartz_cat1}
- {value2}: {schwartz_cat2}
- {value3}: {schwartz_cat3}
- {value4}: {schwartz_cat4}
- {value5}: {schwartz_cat5}
- {value6}: {schwartz_cat6}
- {value7}: {schwartz_cat7}
- {value8}: {schwartz_cat8}
- {value9}: {schwartz_cat9}
- {value10}: {schwartz_cat10}

I am currently aged {age} and based in {country}, with my occupation being {occupation}. Noting the ranked order of my top 5 values and the subsequent 5 values which also hold importance to me, I want you to prepare a detailed analysis and explain the following to me structured as if you are writing a personalised personality diagnostic report.
(a) Considering the placement of these values on the Schwartz Values Wheel, do I have values in conflict or in alignment? Will I experience internal harmony or internal dissonance?
(b) Considering the four higher-order dimensions in Schwartz's work, what does this tell me about my personal inclinations to being open to change or being conservative? What does this tell me about my personal inclinations to transcending oneself or enhancing oneself?

Your response should be formal yet uplifting. This is considered a personality diagnostic report and should only contain body text of no more than 500 words. Hold your response to a high degree of source accuracy with no creativity or hallucination involved in the factual reporting of my values. Noting all of the information you are given about me and my values, this response should be to directly answer the question: Are my values in parallel or in tension?
"""
        },
        {
            "title": "What do my values say about how I make decisions?",
            "question": "What do my values say about how I make decisions?",
            "description": "Decision-making analysis",
            "prompt_template": """
I would like you to reference the research on Functional Theory of Human Values done by Valdiney Gouveia from 1998 to 2018. Ensure that your response to me is based solely on the peer-reviewed and credible research done on this topic. 
My top five values in ranked order from 1st to 5th are {value1}, {value2}, {value3}, {value4}, and {value5}. My subsequent five values in no particular ranked order are {value6}, {value7}, {value8}, {value9}, and {value10}.

I have determined that they correspond very closely to the following Basic Values according to Gouveia:
- {value1}: {gouveia_cat1}
- {value2}: {gouveia_cat2}
- {value3}: {gouveia_cat3}
- {value4}: {gouveia_cat4}
- {value5}: {gouveia_cat5}
- {value6}: {gouveia_cat6}
- {value7}: {gouveia_cat7}
- {value8}: {gouveia_cat8}
- {value9}: {gouveia_cat9}
- {value10}: {gouveia_cat10}

I am currently aged {age} and based in {country}, with my occupation being {occupation}. Noting the ranked order of my top 5 values and the subsequent 5 values which also hold importance to me, I want you to prepare a detailed analysis and explain the following to me structured as if you are writing a personalised personality diagnostic report.
(a) Considering these values in the context of values directing my behaviour toward specific goals, what does this tell me about my decision making and motivations?
(b) Considering these values in the context of values reflecting my needs spectrum between materialism and idealism, what does this tell me about my decision making and motivations?

Your response should be formal yet uplifting. This is considered a personality diagnostic report and should only contain body text of no more than 500 words. Hold your response to a high degree of source accuracy with no creativity or hallucination involved in the factual reporting of my values. Noting all of the information you are given about me and my values, this response should be to directly answer the question: What do my values say about how I make decisions?
"""
        },
        {
            "title": "What do my values say about how I build relationships?",
            "question": "What do my values say about how I build relationships?",
            "description": "Relationship building analysis",
            "prompt_template": """
I would like you to reference the 1992 research on Basic Human Values by Shalom Schwartz and any subsequent studies done with him or based heavily on his work. I would also like you to reference the research on Functional Theory of Human Values done by Valdiney Gouveia from 1998 to 2018. Ensure that your response to me is based solely on the peer-reviewed and credible research done by these two researchers. 
My top five values in ranked order from 1st to 5th are {value1}, {value2}, {value3}, {value4}, and {value5}. 

These values have the following descriptors:
- {value1}: {desc1}
- {value2}: {desc2}
- {value3}: {desc3}
- {value4}: {desc4}
- {value5}: {desc5}
- {value6}: {desc6}
- {value7}: {desc7}
- {value8}: {desc8}
- {value9}: {desc9}
- {value10}: {desc10}

I have determined that they correspond very closely to the following Basic Human Values according to Schwartz:
- {value1}: {schwartz_cat1}
- {value2}: {schwartz_cat2}
- {value3}: {schwartz_cat3}
- {value4}: {schwartz_cat4}
- {value5}: {schwartz_cat5}
- {value6}: {schwartz_cat6}
- {value7}: {schwartz_cat7}
- {value8}: {schwartz_cat8}
- {value9}: {schwartz_cat9}
- {value10}: {schwartz_cat10}

I have determined that they correspond very closely to the following Basic Values according to Gouveia:
- {value1}: {gouveia_cat1}
- {value2}: {gouveia_cat2}
- {value3}: {gouveia_cat3}
- {value4}: {gouveia_cat4}
- {value5}: {gouveia_cat5}
- {value6}: {gouveia_cat6}
- {value7}: {gouveia_cat7}
- {value8}: {gouveia_cat8}
- {value9}: {gouveia_cat9}
- {value10}: {gouveia_cat10}

I am currently aged {age} and based in {country}, with my occupation being {occupation}. Noting the ranked order of my top 5 values and the subsequent 5 values which also hold importance to me, I want you to prepare a detailed analysis and explain the following to me structured as if you are writing a personalised personality diagnostic report.
(a) Considering where my values are at on the Schwartz Values Wheel and on the Gouveia Two-by-Three Framework of Core Functions, how might I communicate?
(b) Considering where my values are at on the Schwartz Values Wheel and on the Gouveia Two-by-Three Framework of Core Functions, what might I seek in relationships in general?
(c) Considering where my values are at on the Schwartz Values Wheel and on the Gouveia Two-by-Three Framework of Core Functions, what relationship dynamics would be more fulfilling for me and what relationship dynamics would be more challenging for me?

Your response should be formal yet uplifting. This is considered a personality diagnostic report and should only contain body text of no more than 500 words. Hold your response to a high degree of source accuracy with no creativity or hallucination involved in the factual reporting of my values. Noting all of the information you are given about me and my values, this response should be to directly answer the question: What do my values say about how I build relationships?
"""
        }
    ]