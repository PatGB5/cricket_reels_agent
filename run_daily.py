from app.agents.fact_agent import CricketFactAgent
from app.agents.script_agent import ScriptAgent
# from app.agents.fact_agent import get_facts
# from app.services.image_downloader import download_images_from_facts
if __name__ == "__main__":
    fact_agent = CricketFactAgent(
        credentials_path="salk-ai-app-83f08d5d8778.json",
        project="salk-ai-app",
        location="us-central1"
    )
    script_agent = ScriptAgent(
        credentials_path="salk-ai-app-83f08d5d8778.json",
        project="salk-ai-app",
        location="us-central1"
    )
    # facts =  [
    #             {
    #             "fact": "On May 22, 1936, the foundation stone for Brabourne Stadium, India's first cricket stadium, was laid in Bombay."
    #             },
    #             {
    #             "fact": "On May 22, 1907, Albert Trott became the first bowler to take two hat-tricks in a single innings during a match for Middlesex against Somerset at Lord's."
    #             },
    #             {
    #             "fact": "Indian off-spinner Erapalli Prasanna, known as one of India's great spinners, was born on May 22, 1940."
    #             },
    #             {
    #             "fact": "Sarfaraz Ahmed, the Pakistani wicketkeeper-batsman who captained his team to victory in the 2017 Champions Trophy, was born on May 22, 1987."
    #             },
    #             {
    #             "fact": "On May 22, 2010, the first-ever official T20 International match on American soil was played between New Zealand and Sri Lanka in Lauderhill, Florida."
    #             }
    #         ]
    facts = fact_agent.get_facts()
    print("\n--- Cricket Facts ---\n", facts)    
    # facts_with_images = download_images_from_facts(facts)
    # script = script_agent.generate_script(facts)
    # print("\n--- Generated Script ---\n", script)