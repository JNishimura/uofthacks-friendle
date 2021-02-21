VECTOR_LENGTH = 63

MBTI_TO_INDEX = {
    "INTJ": 0,
    "INTP": 1,
    "ENTJ": 2,
    "ENTP": 3,
    "INFJ": 4,
    "INFP": 5,
    "ENFJ": 6,
    "ENFP": 7,
    "ISTJ": 8,
    "ISFJ": 9,
    "ESTJ": 10,
    "ESFJ": 11,
    "ISTP": 12,
    "ISFP": 13,
    "ESTP": 14,
    "ESFP": 15
}

MBTI_COMPATIBILITY = {
    "INTJ": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP"],
        "medium": ["ISFP", "ESFP", "ISTP", "ESTP"],
        "low": ["ISFJ", "ESFJ", "ISTJ", "ESTJ"]
    },
    "INTP": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP", "ESTJ"],
        "medium": ["ISFP", "ESFP", "ISTP", "ESTP"],
        "low": ["ISFJ", "ESFJ", "ISTJ"]
    },
    "ENTJ": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP"],
        "medium": ["ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
        "low": []
    },
    "ENTP": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP"],
        "medium": ["ISFP", "ESFP", "ISTP", "ESTP"],
        "low": ["ISFJ", "ESFJ", "ISTJ", "ESTJ"]
    },
    "INFJ": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP"],
        "medium": [],
        "low": ["ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"]
    },
    "INFP": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP"],
        "medium": [],
        "low": ["ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"]
    },
    "ENFJ": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP", "ISFP"],
        "medium": [],
        "low": ["ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"]
    },
    "ENFP": {
        "high": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP"],
        "medium": [],
        "low": ["ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"]
    },
    "ISTJ": {
        "high": ["ESFP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
        "medium": ["ENTJ", "ISFP", "ISTP"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "INTP", "ENTP"]
    },
    "ISFJ": {
        "high": ["ESFP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
        "medium": ["ENTJ", "ISFP", "ISTP"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "INTP", "ENTP"]
    },
    "ESTJ": {
        "high": ["INTP", "ISFP", "ISTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
        "medium": ["ENTJ", "ESFP", "ESTP"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTP"]
    },
    "ESFJ": {
        "high": ["ISFP", "ISTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
        "medium": ["ENTJ", "ESFP", "ESTP"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "INTP", "ENTP"]
    },
    "ISTP": {
        "high": ["ESFJ", "ESTJ"],
        "medium": ["INTJ", "ENTJ", "INTP", "ENTP", "ISFJ", "ISTJ"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "ISFP", "ESFP", "ISTP", "ESTP"]
    },
    "ISFP": {
        "high": ["ENFJ", "ESFJ", "ESTJ"],
        "medium": ["INTJ", "ENTJ", "INTP", "ENTP", "ISFJ", "ISTJ"],
        "low": ["INFP", "ENFP", "INFJ", "ISFP", "ESFP", "ISTP", "ESTP"]
    },
    "ESTP": {
        "high": ["ISFJ", "ISTJ"],
        "medium": ["INTJ", "ENTJ", "INTP", "ENTP", "ESFJ", "ESTJ"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "ISFP", "ESFP", "ISTP", "ESTP"]
    },
    "ESFP": {
        "high": ["ISFJ", "ISTJ"],
        "medium": ["INTJ", "ENTJ", "INTP", "ENTP", "ESFJ", "ESTJ"],
        "low": ["INFP", "ENFP", "INFJ", "ENFJ", "ISFP", "ESFP", "ISTP", "ESTP"]
    }
}

MUSIC_TO_INDEX = {
    "ANIME": 16,
    "CLASSICAL": 17,
    "COUNTRY": 18,
    "EDM": 19,
    "FOLK": 20,
    "HIP-HOP": 21,
    "INDIE": 22,
    "JAZZ": 23,
    "K-POP": 24,
    "POP": 25,
    "R-N-B": 26,
    "ROCK": 27
}

MOVIE_TO_INDEX = {
    "ACTION": 28,
    "ADVENTURE": 29,
    "ANIMATION": 30,
    "COMEDY": 31,
    "DOCUMENTARY": 32,
    "DRAMA": 33,
    "FANTASY": 34,
    "HORROR": 35,
    "MYSTERY": 36,
    "ROMANCE": 37,
    "SCI-FI": 38,
    "THRILLER": 39
}

FOOD_TO_INDEX = {
    "AMERICAN": 40,
    "ASIAN FUSION": 41,
    "BREAKFAST & BRUNCH": 42,
    "CAFES": 43,
    "CHINESE": 44,
    "FRENCH": 45,
    "ITALIAN": 46,
    "JAPANESE": 47,
    "MEDITERRANEAN": 48,
    "MEXICAN": 49,
    "SOUL FOOD": 50
}

GAME_TO_INDEX = {
    "APEX LEGENDS": 51,
    "CALL OF DUTY": 52,
    "CS:GO": 53,
    "DOTA 2": 54,
    "FORTNITE": 55,
    "GENSHIN IMPACT": 56,
    "GTA V": 57,
    "LEAGUE OF LEGENDS": 58,
    "MINECRAFT": 59,
    "NBA 2K": 60,
    "ROCKET LEAGUE": 61,
    "VALORANT": 62
}