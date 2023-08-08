from youtube_transcript_api import YouTubeTranscriptApi

def getSubtitle(ID):
    # 동영상의 자막 정보 조회
    transcript_list = YouTubeTranscriptApi.list_transcripts(ID)

    # 한국어 (ko) 자막 가져오기
    korean_transcript = transcript_list.find_transcript(['ko']).fetch()

    # korean_transcript 변수에 한국어 자막 내용 저장
    print(korean_transcript)

# ID1 = 'mdNZI3TKR0I'
# getSubtitle(ID1)
# arrWord = []
