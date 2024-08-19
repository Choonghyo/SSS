from google.cloud import translate_v2 as translate

def translate_text(target, text):
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]

def main():
    # 영어로 변환된 텍스트
    english_text = """gunshot on Wong 90th I I don't know the place is just very busy lately I I don't know what's going on this is the second shooting incident in less than a week  working at a flower shop was hit by a stray bullet on Saturday afternoon no arrests in either case  in the University Heights section of the Bronx Market Souls Channel 7 Eyewitness News  a 3-year old little boy is now a critical condition after police say he accidentally turned a loaded gun on himself"""
    
    # 한국어로 번역
    korean_text = translate_text("ko", english_text)
    print("Korean Text:", korean_text)

if __name__ == "__main__":
    main()
