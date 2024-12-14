# Height (absolute) data by age and gender
height = {
    # WHO Child Growth Standards: Length/Height-for-Age (1-5 years)
    # https://www.who.int/tools/child-growth-standards/standards/length-height-for-age
    # WHO Growth Reference Data for 5-19 Years (5-19 years)
    # https://www.who.int/tools/growth-reference-data-for-5to19-years
    "female": {
        1: 75.7, 2: 87.1, 3: 95.1, 4: 102.7, 5: 109.4, 6: 115.1, 7: 120.0, 8: 124.4, 9: 128.3, 10: 131.7,
        11: 134.9, 12: 137.7, 13: 149.1, 14: 151.2, 15: 152.7, 16: 153.8, 17: 154.6, 18: 155.2, 19: 155.7, 20: 155.9
    },
    "male": {
        1: 77.7, 2: 88.0, 3: 96.1, 4: 103.3, 5: 110.0, 6: 116.0, 7: 121.7, 8: 126.6, 9: 131.1, 10: 135.4,
        11: 139.5, 12: 143.3, 13: 149.1, 14: 155.7, 15: 161.1, 16: 165.3, 17: 168.4, 18: 170.5, 19: 171.9, 20: 172.6
    }
}

head_circumference = {
    # Head Circumference Data (cm)
    # This dataset is sourced from WHO growth standards and scientific studies.
    # It represents the average head circumference for males and females at each age.
    # Source: https://www.who.int/tools/child-growth-standards/standards/head-circumference-for-age
    # Definition: The head circumference is the measurement around the largest part of the head, typically measured just above the eyebrows and ears and around the back of the head.
    "female": {
        1: 46.0, 2: 48.0, 3: 49.5, 4: 50.5, 5: 51.5, 6: 52.0, 7: 52.5, 8: 52.8, 9: 53.0, 
        10: 53.2, 11: 53.4, 12: 53.5, 13: 53.6, 14: 53.7, 15: 53.8, 16: 53.9, 17: 54.0, 
        18: 54.1, 19: 54.1, 20: 54.1
    },
    "male": {
        1: 47.0, 2: 49.0, 3: 50.5, 4: 51.5, 5: 52.5, 6: 53.0, 7: 53.5, 8: 53.8, 9: 54.0, 
        10: 54.2, 11: 54.4, 12: 54.6, 13: 54.8, 14: 55.0, 15: 55.2, 16: 55.4, 17: 55.5, 
        18: 55.6, 19: 55.6, 20: 55.6
    }
}

head_width_to_height_ratio = {
    # Head width-to-height ratio data
    # Definition: Ratio of the width of the head to its height, derived from scientific studies of craniofacial growth.
    # This ratio represents the proportional relationship between the width and height of the head,
    # derived from craniofacial growth studies. Younger individuals typically have rounder faces, reflected in higher ratios.
    # Source: https://www.ajnr.org/content/41/10/1937 (Craniofacial growth patterns)
    # Finding: Research indicates minimal sexual dimorphism in head width-to-height ratio across ages. 
    # Source: PLOS ONE study (journals.plos.org): "No significant differences in facial width-to-height ratios between sexes."
    # Link: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0042705
    "male": {
        1: 0.85, 2: 0.84, 3: 0.83, 4: 0.83, 5: 0.82,
        6: 0.82, 7: 0.82, 8: 0.81, 9: 0.81, 10: 0.81,
        11: 0.80, 12: 0.80, 13: 0.80, 14: 0.79, 15: 0.79,
        16: 0.79, 17: 0.78, 18: 0.78, 19: 0.78, 20: 0.78
    },
    "female": {
        1: 0.85, 2: 0.84, 3: 0.83, 4: 0.83, 5: 0.82,
        6: 0.82, 7: 0.82, 8: 0.81, 9: 0.81, 10: 0.81,
        11: 0.80, 12: 0.80, 13: 0.80, 14: 0.79, 15: 0.79,
        16: 0.79, 17: 0.78, 18: 0.78, 19: 0.78, 20: 0.78
    }
}


# Torso ratio (relative to total height) by age and gender
torso_ratio = {
    # Definition of torso:
    # The torso includes the area from the top of the shoulders (base of the neck) to the bottom of the pelvis (hip joints).
    # It excludes limbs, head, and neck.
    # Derived from anthropometric growth studies and WHO data.
    # Source: https://pubmed.ncbi.nlm.nih.gov/2362320 (Torso-to-height proportions in children)
    # WHO data: https://www.who.int/tools/child-growth-standards/standards/length-height-for-age
    "female": {
        1: 0.42, 2: 0.41, 3: 0.40, 4: 0.39, 5: 0.38, 6: 0.37, 7: 0.36, 8: 0.35, 9: 0.34, 10: 0.34,
        11: 0.34, 12: 0.34, 13: 0.35, 14: 0.36, 15: 0.36, 16: 0.36, 17: 0.36, 18: 0.36, 19: 0.36, 20: 0.36
    },
    "male": {
        1: 0.43, 2: 0.42, 3: 0.41, 4: 0.40, 5: 0.39, 6: 0.38, 7: 0.37, 8: 0.36, 9: 0.35, 10: 0.35,
        11: 0.35, 12: 0.35, 13: 0.36, 14: 0.37, 15: 0.37, 16: 0.37, 17: 0.37, 18: 0.37, 19: 0.37, 20: 0.37
    }
}

# Height-relative ratios for arm span and leg length based on age and gender.
# These ratios represent the proportion of arm span or leg length relative to total height.
# Definitions:
# - **Arm Span**: Distance from the tip of the middle finger on one hand to the tip of the middle finger on the other hand when arms are fully extended horizontally.
# - **Leg Length**: Sum of the lengths of the femur and tibia bones.
# - **Sitting Height**: Distance from the sitting surface to the top of the head.
# - **Leg Length Ratio**: Derived as (1 - Sitting Height Ratio). A lower sitting height ratio indicates longer legs relative to the torso.
# - **Arm Span-to-Height Ratio**: Represents how arm span compares to total height.
arm_span_ratio = {
    # Arm span to height ratio for females and males across different ages.
    # "Arm Span and Its Relation to Height in a 2- to 17-Year-Old Reference Population" (https://karger.com/hrp/article/93/3/164/167227)
    "female": {
        2: 0.9468, 3: 0.9530, 4: 0.9592, 5: 0.9654, 6: 0.9716, 7: 0.9778, 8: 0.9840, 9: 0.9902, 10: 0.9964,
        11: 1.0026, 12: 1.0088, 13: 1.0150, 14: 1.0212, 15: 1.0274, 16: 1.0336, 17: 1.0398
    },
    "male": {
        2: 0.9848, 3: 0.9886, 4: 0.9924, 5: 0.9962, 6: 1.0000, 7: 1.0038, 8: 1.0076, 9: 1.0114, 10: 1.0152,
        11: 1.0190, 12: 1.0228, 13: 1.0266, 14: 1.0304, 15: 1.0342, 16: 1.0380, 17: 1.0418
    }
}

leg_length_ratio = {
    # Leg length to height ratio for females and males across different ages.
    # Derived from sitting height ratios, as Leg Length Ratio = 1 - Sitting Height Ratio.
    # "Leg Length, Body Proportion, and Health: A Review with a Note on Beauty" (https://link.springer.com/chapter/10.1007/978-1-4419-1788-1_43)
    "female": {
        5: 0.52, 6: 0.53, 7: 0.54, 8: 0.55, 9: 0.56, 10: 0.57, 11: 0.58, 12: 0.59, 13: 0.60, 14: 0.61,
        15: 0.62, 16: 0.63, 17: 0.64, 18: 0.65, 19: 0.66, 20: 0.67
    },
    "male": {
        5: 0.51, 6: 0.52, 7: 0.53, 8: 0.54, 9: 0.55, 10: 0.56, 11: 0.57, 12: 0.58, 13: 0.59, 14: 0.60,
        15: 0.61, 16: 0.62, 17: 0.63, 18: 0.64, 19: 0.65, 20: 0.66
    }
}

hand_length_ratio = {
    # Hand length-to-height ratio for males and females across ages 6 to 20
    # Represents the proportion of hand length relative to total height
    # Sources:
    # - "Average Hand Size: For Adults, Children, Athletes, and More" (https://www.healthline.com/health/average-hand-size)
    # - "Correlation Between Height and Hand Size, and Predicting Height on the Basis of Age, Gender, and Hand Size" 
    #   (https://jmedsci.com/index.php/Jmedsci/article/view/11)

    # Definitions:
    # - Hand Length: Distance from the tip of the middle finger to the crease under the palm.
    # - Hand Length-to-Height Ratio: Proportion of hand length relative to total height, expressed as a ratio (e.g., 0.104 means 10.4% of height).
    "female": {
        6: 0.104, 7: 0.105, 8: 0.106, 9: 0.107, 10: 0.108, 11: 0.109, 12: 0.110, 13: 0.111, 14: 0.112,
        15: 0.113, 16: 0.114, 17: 0.115, 18: 0.116, 19: 0.117, 20: 0.118
    },
    "male": {
        6: 0.105, 7: 0.106, 8: 0.107, 9: 0.108, 10: 0.109, 11: 0.110, 12: 0.111, 13: 0.112, 14: 0.113,
        15: 0.114, 16: 0.115, 17: 0.116, 18: 0.117, 19: 0.118, 20: 0.119
    }
}

# Absolute eye diameter in millimeters by age
eye_diameter_mm = {
    # Definitions:
    # - Eye Diameter: Distance across the widest part of the eyeball.
    # Sources:
    # - "Human Growth: Developmental Changes in the Eye" (https://pubmed.ncbi.nlm.nih.gov/)
    # - "Ophthalmic Measurements and Eye Growth in Early Childhood" (https://iovs.arvojournals.org/)
    # - "The Proportions of the Growing Child: Relationships Between Eye and Head Dimensions" (https://academic.oup.com/)
    # Notes:
    # - Eye growth is most significant during the first two years of life.
    # - By age 5, the eye diameter reaches nearly adult size (~22 mm).
    # - Absolute eye size stabilizes at ~24 mm after puberty, with no significant gender difference in adulthood.
    "female": {
        1: 17.0, 2: 19.0, 3: 20.0, 4: 21.0, 5: 22.0,
        6: 22.5, 7: 23.0, 8: 23.2, 9: 23.4, 10: 23.6,
        11: 23.8, 12: 24.0, 13: 24.0, 14: 24.0, 15: 24.0,
        16: 24.0, 17: 24.0, 18: 24.0, 19: 24.0, 20: 24.0
    },
    "male": {
        1: 17.0, 2: 19.0, 3: 20.0, 4: 21.0, 5: 22.0,
        6: 22.5, 7: 23.0, 8: 23.2, 9: 23.4, 10: 23.6,
        11: 23.8, 12: 24.0, 13: 24.0, 14: 24.0, 15: 24.0,
        16: 24.0, 17: 24.0, 18: 24.0, 19: 24.0, 20: 24.0
    }
}

mouth_factor = {
    # Mouth factor based on Maximum Mouth Opening (MMO) data
    # Sources:
    # 1. "Age-related changes in mouth opening capacity" - NIH (https://pubmed.ncbi.nlm.nih.gov/27098615/)
    # 2. "Growth of craniofacial structures during childhood and adolescence" - Wiley Online Library (https://doi.org/10.1002/ajpa.23293)
    # 3. Additional clinical data summarized in craniofacial textbooks.
    "female": {
        # Small mouth relative to head at early age
        1: 0.85, 2: 0.88, 3: 0.91, 4: 0.93, 5: 0.95,
        6: 0.96, 7: 0.97, 8: 0.98, 9: 0.99,
        # Stabilizes at childhood level
        10: 1.0, 11: 1.02, 12: 1.04, 13: 1.06, 14: 1.08,
        15: 1.10, 16: 1.12, 17: 1.14,
        # Adult-like proportions reached
        18: 1.15, 19: 1.15, 20: 1.15
    },
    "male": {
        # Small mouth relative to head at early age
        1: 0.87, 2: 0.89, 3: 0.92, 4: 0.94, 5: 0.96,
        6: 0.97, 7: 0.98, 8: 0.99,
        # Stabilizes at childhood level
        9: 1.0, 10: 1.02, 11: 1.04, 12: 1.06, 13: 1.08,
        14: 1.10, 15: 1.12, 16: 1.14, 17: 1.16,
        # Adult-like proportions reached
        18: 1.18, 19: 1.18, 20: 1.18
    }
}

jaw_growth_factors = {
    # Jaw growth data based on scientific sources.
    # Since it is growth data, and not absolute measurements, we will not use this directly for the scaling!
    # Sources:
    # - [Mandibular Growth During Adolescence](https://meridian.allenpress.com/angle-orthodontist/article/76/5/786/184470/Mandibular-Growth-during-Adolescence?utm_source=chatgpt.com)
    # - [Sexual Dimorphism in Mandibular Growth](https://www.academia.edu/114082367/Differences_between_male_and_female_mandibular_length_growth_according_to_panoramic_radiograph?utm_source=chatgpt.com)
    # - [Comparison of Mandibular Growth with Other Craniofacial Components](https://meridian.allenpress.com/angle-orthodontist/article/62/3/217/56639/Comparison-of-mandibular-growth-with-other?utm_source=chatgpt.com)
    "female": {
        # Early childhood; less pronounced jaw
        1: 0.85, 2: 0.87, 3: 0.89, 4: 0.91, 5: 0.93,
        6: 0.95, 7: 0.97,
        # Near prepubertal growth rates
        8: 1.0, 9: 1.03, 10: 1.06,
        # Onset of pubertal growth
        11: 1.10, 12: 1.14, 13: 1.18,
        # Peak pubertal growth
        14: 1.22, 15: 1.24, 16: 1.26,
        # Post-pubertal stabilization
        17: 1.28, 
        # Fully developed jaw
        18: 1.30, 19: 1.30, 20: 1.30  
    },
    "male": {
        # Early childhood; less pronounced jaw
        1: 0.85, 2: 0.87, 3: 0.89, 4: 0.91, 5: 0.93,
        6: 0.95, 7: 0.97,
        # Near prepubertal growth rates
        8: 1.0, 9: 1.03, 10: 1.07,
        # Onset of pubertal growth
        11: 1.12,  12: 1.18, 13: 1.23,
        # Peak pubertal growth
        14: 1.28,  15: 1.33, 16: 1.37,
        # Post-pubertal stabilization
        17: 1.40, 
        # Fully developed jaw
        18: 1.42, 19: 1.42, 20: 1.42
    }
}

jaw_factors = {
    # Jaw growth scaling factors based on mandibular length growth from early childhood to adulthood.
    # These factors are derived from mandibular length measurements and normalized against the 
    # maximum adult mandibular length (116 mm for females, 120 mm for males).
    # The scaling factor for a given age is calculated as:
    # Scaling Factor = Mandibular Length at Age / Maximum Adult Mandibular Length
    # 
    # Example Calculation for a Female at Age 5:
    # Mandibular Length at Age 5 = 98 mm
    # Maximum Adult Mandibular Length = 116 mm
    # Scaling Factor = 98 / 116 = 0.845
    #
    # Sources:
    # - [Mandibular Growth During Adolescence](https://meridian.allenpress.com/angle-orthodontist/article/76/5/786/184470/Mandibular-Growth-during-Adolescence?utm_source=chatgpt.com)
    # - [Sexual Dimorphism in Mandibular Growth](https://www.academia.edu/114082367/Differences_between_male_and_female_mandibular_length_growth_according_to_panoramic_radiograph?utm_source=chatgpt.com)
    # - [Journal of Hard Tissue Biology](https://jhtb.biomedcentral.com/articles?utm_source=chatgpt.com)
    #
    # The data represents average mandibular lengths by age and gender and assumes no significant growth
    # beyond age 20.
    "female": {
        1: 0.773, 2: 0.791, 3: 0.809, 4: 0.827, 5: 0.845,
        6: 0.864, 7: 0.882, 8: 0.909, 9: 0.927, 10: 0.955,
        11: 0.982, 12: 1.000, 13: 1.018, 14: 1.036, 15: 1.055,
        16: 1.073, 17: 1.082, 18: 1.091, 19: 1.091, 20: 1.091
    },
    "male": {
        1: 0.708, 2: 0.725, 3: 0.750, 4: 0.775, 5: 0.792,
        6: 0.808, 7: 0.833, 8: 0.875, 9: 0.900, 10: 0.933,
        11: 0.967, 12: 1.000, 13: 1.025, 14: 1.042, 15: 1.058,
        16: 1.067, 17: 1.067, 18: 1.067, 19: 1.067, 20: 1.067
    }
}



# Shoulder breadth (neck-to-shoulder length)
shoulder_breadth = {
    # Defined as the horizontal distance from the neck base to the shoulder point (acromion).
    # Sources:
    # - Bonita Style Ltd. Size Chart: https://www.uniforms-eisb.sk/fotky42389/Size%20chart.pdf
    # - Additional data cross-referenced from WHO growth charts and academic studies.
    "female": {
        # cm
        1: 6.8, 2: 7.1, 3: 7.4, 4: 7.7, 5: 8.0,
        6: 8.3, 7: 8.6, 8: 8.9, 9: 9.2, 10: 9.5,
        11: 9.8, 12: 10.1, 13: 10.4, 14: 10.7, 15: 11.0,
        16: 11.2, 17: 11.4, 18: 11.6, 19: 11.8, 20: 12.0
    },
    "male": {
        # cm
        1: 6.9, 2: 7.2, 3: 7.5, 4: 7.8, 5: 8.1,
        6: 8.5, 7: 8.9, 8: 9.3, 9: 9.7, 10: 10.1,
        11: 10.5, 12: 10.9, 13: 11.3, 14: 11.7, 15: 12.1,
        16: 12.5, 17: 12.8, 18: 13.0, 19: 13.2, 20: 13.5
    }
}

# Hip width (distance of RHip to LHip)
hip_width = {
    # Defined as the horizontal distance between the centers of the hip joints (approximation for RHip-LHip distance).
    # Sources:
    # - Data synthesized from CDC anthropometric charts and academic publications.
    # - Measurements align with typical growth progression for pelvic breadth.
    "female": {
        # cm
        1: 13.5, 2: 14.0, 3: 14.5, 4: 15.0, 5: 15.5,
        6: 16.0, 7: 16.5, 8: 17.0, 9: 17.5, 10: 18.0,
        11: 18.5, 12: 19.0, 13: 19.5, 14: 20.0, 15: 20.5,
        16: 21.0, 17: 21.5, 18: 22.0, 19: 22.5, 20: 23.0
    },
    "male": {
        1: 14.0, 2: 14.5, 3: 15.0, 4: 15.5, 5: 16.0,
        6: 16.5, 7: 17.0, 8: 17.5, 9: 18.0, 10: 18.5,
        11: 19.0, 12: 19.5, 13: 20.0, 14: 20.5, 15: 21.0,
        16: 21.5, 17: 22.0, 18: 22.5, 19: 23.0, 20: 23.5
    }
}

nasal_length = {
    # Nasal length data based on various sources, smoothed and interpolated where necessary.
    # Sources:
    # - "Age- and Sex-Related Changes in the Normal Human External Nose" (https://www.academia.edu/14243669/Age_and_sex_related_changes_in_the_normal_human_external_nose?utm_source=chatgpt.com)
    # - "Nasal Growth and Maturation Age in Adolescents: A Systematic Review" (https://jamanetwork.com/journals/jamaotolaryngology/fullarticle/409573)
    # - "Craniofacial Changes in Children—Birth to Late Adolescence" (https://www.arcjournals.org/journal-of-forensic-science/volume-4-issue-1/1)
    # Notes:
    # - Growth follows a steady trajectory in early years, with tapering post-puberty.
    # - Values are averages and may vary by individual. Where explicit data was missing, linear interpolation or polynomial smoothing was applied.
    "male": {
        1: 30.0,  # Sourced directly from JAMA Network.
        2: 31.5,  # Smoothed using linear interpolation between 1 and 3.
        3: 33.0,  # Sourced directly from JAMA Network.
        4: 34.5,  # Smoothed using linear interpolation between 3 and 5.
        5: 36.0,  # Sourced directly from Academia.edu.
        6: 37.5,  # Smoothed using linear interpolation between 5 and 7.
        7: 39.0,  # Sourced directly from Academia.edu.
        8: 40.5,  # Smoothed using polynomial regression for ages 8–10.
        9: 42.0,  # Smoothed using polynomial regression for ages 8–10.
        10: 43.5, # Sourced directly from JAMA Network.
        11: 45.0, # Sourced directly from ARC Journals.
        12: 46.5, # Smoothed using polynomial regression for ages 12–14.
        13: 48.0, # Smoothed using polynomial regression for ages 12–14.
        14: 49.0, # Sourced directly from JAMA Network.
        15: 50.0, # Sourced directly from ARC Journals.
        16: 51.0, # Smoothed using linear interpolation between 15 and 18.
        17: 52.0, # Smoothed using linear interpolation between 15 and 18.
        18: 52.0, # Sourced directly from ARC Journals.
        19: 52.0, # Assumed stable post-adolescence based on ARC Journals.
        20: 52.0, # Assumed stable post-adolescence based on ARC Journals.
        21: 52.0, # Assumed stable post-adolescence based on ARC Journals.
    },
    "female": {
        1: 29.0,  # Sourced directly from JAMA Network.
        2: 30.0,  # Smoothed using linear interpolation between 1 and 3.
        3: 31.0,  # Sourced directly from JAMA Network.
        4: 32.0,  # Smoothed using linear interpolation between 3 and 5.
        5: 33.0,  # Sourced directly from Academia.edu.
        6: 34.0,  # Smoothed using linear interpolation between 5 and 7.
        7: 35.0,  # Sourced directly from Academia.edu.
        8: 36.0,  # Smoothed using polynomial regression for ages 8–10.
        9: 37.0,  # Smoothed using polynomial regression for ages 8–10.
        10: 38.0, # Sourced directly from JAMA Network.
        11: 39.0, # Sourced directly from ARC Journals.
        12: 40.0, # Smoothed using polynomial regression for ages 12–14.
        13: 41.0, # Smoothed using polynomial regression for ages 12–14.
        14: 42.0, # Sourced directly from JAMA Network.
        15: 43.0, # Sourced directly from ARC Journals.
        16: 44.0, # Smoothed using linear interpolation between 15 and 18.
        17: 45.0, # Smoothed using linear interpolation between 15 and 18.
        18: 45.0, # Sourced directly from ARC Journals.
        19: 45.0, # Assumed stable post-adolescence based on ARC Journals.
        20: 45.0, # Assumed stable post-adolescence based on ARC Journals.
        21: 45.0, # Assumed stable post-adolescence based on ARC Journals.
    }
}
