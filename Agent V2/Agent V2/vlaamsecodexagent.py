import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from tools import zoek_vlaamse_codex_api, vind_relatie, krijg_voorlaatste_versie, krijg_beschikbare_tools

# Laad omgevingsvariabelen
load_dotenv()

class VlaamseCodexAgent:
    """
    Vlaamse Codex Agent die Claude laat beslissen welke tools te gebruiken voor wetgevingsanalyse.
    Gespecialiseerd in het analyseren van drukproeven en consolidatie van Vlaamse wetgeving.
    """
    
    def __init__(self):
        # Initialiseer Anthropic client met API key uit environment
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please check your .env file.")
        
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
        
        # Krijg beschikbare tools en converteer naar Claude's tool formaat
        self.tools = self._converteer_tools_formaat()
        self.tool_functies = {
            "zoek_vlaamse_codex_api": zoek_vlaamse_codex_api,
            "vind_relatie": vind_relatie,
            "krijg_voorlaatste_versie": krijg_voorlaatste_versie
        }
        
        # Initialize Anthropic client without proxies
        self.client = Anthropic(api_key=self.anthropic_api_key)
        
        print(f"🛠️  Beschikbare tools: {list(self.tool_functies.keys())}")
        print()

    def _converteer_tools_formaat(self):
        """Converteer onze tool definities naar Claude's verwachte formaat."""
        tools = krijg_beschikbare_tools()
        claude_tools = []
        
        for tool in tools:
            claude_tools.append({
                "name": tool['name'],
                "description": tool['description'],
                "input_schema": tool['parameters']
            })
        
        return claude_tools

    def _voer_tool_uit(self, tool_naam: str, parameters: dict):
        """Voer een tool functie uit met gegeven parameters."""
        if tool_naam in self.tool_functies:
            try:
                resultaat = self.tool_functies[tool_naam](**parameters)
                
                # Speciale behandeling voor krijg_voorlaatste_versie om inhoud vast te leggen
                if tool_naam == "krijg_voorlaatste_versie" and resultaat.get('succes'):
                    document_id = parameters.get('document_id')
                    inhoud = resultaat.get('inhoud', '')
                    print(f"📄 Document {document_id} succesvol opgehaald")
                    # Bewaar op een globale manier die toegankelijk is voor de Flask app
                    if hasattr(self, '_document_callback'):
                        self._document_callback(document_id, inhoud)
                
                return resultaat
            except Exception as e:
                print(f"❌ Tool mislukt: {e}")
                return {"succes": False, "fout": str(e)}
        else:
            print(f"❌ Onbekende tool: {tool_naam}")
            return {"succes": False, "fout": f"Onbekende tool: {tool_naam}"}

    def voer_uit(self):
        """Voer de agent uit - laat Claude beslissen wat te doen met de drukproef."""
        # Lees het drukproef bestand vanuit de huidige directory
        bestand_pad = 'drukproef.md'
        
        try:
            with open(bestand_pad, 'r', encoding='utf-8') as f:
                drukproef_tekst = f.read()
        except Exception as e:
            print(f"❌ Fout bij lezen bestand: {e}")
            return

        print(f"📄 Drukproef geladen van {bestand_pad}")
     
        # Initiële systeem prompt in het Nederlands
        systeem_prompt = """Je bent een expert agent voor het analyseren van Vlaamse drukproef documenten. 

BELANGRIJK: Begin ALTIJD met een korte uitleg van wat je gaat doen en waarom, voordat je tools gebruikt.

Je doel is om:
1. De drukproef te analyseren om te begrijpen welke wetgeving wordt gerefereerd
2. De beschikbare tools te gebruiken om de gerefereerde wetgeving te vinden in de Vlaamse Codex
3. Originele besluiten en hun wijzigingsgeschiedenis te identificeren. Lijst ze op ID en de datum van de wijziging.
4. ALLEEN NADAT je het originele document ID hebt gevonden, gebruik krijg_voorlaatste_versie om de werkelijke inhoud op te halen
5. Een uitgebreide analyse te geven van wat er allemaal moet veranderen door de drukproef. Geef enkel de wijzigingen weer

BELANGRIJKE WORKFLOW:
- Eerst: Gebruik zoek_vlaamse_codex_api en vind_relatie om het originele document ID te identificeren
- Tweede: Zodra je het originele document ID hebt, gebruik krijg_voorlaatste_versie om de volledige inhoud te krijgen
- Derde: Analyseer zowel de drukproef als het originele document om te tonen welke wijzigingen worden gemaakt

ZOEKSTRATEGIE TIPS:
- Gebruik exacte volzinnen zoals ze in de drukproef staan. De API zoekt letterlijk. De correcte wetgeving staat er altijd in. Er zijn vaak meerdere versies van dezelfde wetgeving of besluiten die wetgeving aanpassen
- wijzingsbesluiten hebben altijd een relatie met het origineledocument

VERPLICHT FORMAAT:
1. Leg eerst uit wat je gaat doen en waarom je een tool kiest (1 zin)
2. Gebruik dan de juiste tool(s)
3. Analyseer de resultaten

Je hebt toegang tot tools die de Vlaamse codex API kunnen doorzoeken, documentrelaties kunnen vinden, en documentinhoud kunnen ophalen. Gebruik ze strategisch en in de juiste volgorde.
Wees adaptief - als één aanpak niet goed werkt, probeer verschillende zoektermen of strategieën."""

        # Start het gesprek
        berichten = [
            {
                "role": "user", 
                "content": f"Analyseer het drukproef document en vind de gerefereerde wetgeving:\n\n{drukproef_tekst}"
            }
        ]

        # Agent loop - laat Claude de flow controleren
        max_iteraties = 10
        iteratie = 0
        
        while iteratie < max_iteraties:
            iteratie += 1
            print(f"📋 Agent stap {iteratie}")
            
            try:
                # Stuur bericht naar Claude met beschikbare tools
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    system=systeem_prompt,
                    messages=berichten,
                    tools=self.tools
                )
                
                # Controleer of Claude tools wil gebruiken
                if response.stop_reason == "tool_use":
                    # Toon Claude's nadenkstappen en tool keuzes
                    heeft_tekst = False
                    for content_block in response.content:
                        if content_block.type == "text" and content_block.text.strip():
                            if not heeft_tekst:
                                print("🧠 Codex agent denkt:")
                            
                                heeft_tekst = True
                            print(content_block.text)
                    
                    # Toon welke tools Claude wil gebruiken
                    print("🛠️ codex agent kiest tools:")
                    for content_block in response.content:
                        if content_block.type == "tool_use":
                            print(f"   → {content_block.name} met parameters: {content_block.input}")
                    print()
                    
                    # Claude wil tools gebruiken
                    tool_resultaten = []
                    
                    for content_block in response.content:
                        if content_block.type == "tool_use":
                            # Voer de tool uit die Claude heeft gevraagd
                            tool_naam = content_block.name
                            tool_params = content_block.input
                            tool_id = content_block.id
                            
                            resultaat = self._voer_tool_uit(tool_naam, tool_params)
                            
                            tool_resultaten.append({
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": json.dumps(resultaat)
                            })
                    
                    # Voeg Claude's response en tool resultaten toe aan gesprek
                    berichten.append({"role": "assistant", "content": response.content})
                    berichten.append({"role": "user", "content": tool_resultaten})
                    
                else:
                    # Claude is klaar, toon finale response
                    for content_block in response.content:
                        if content_block.type == "text":
                            print(content_block.text)
                    break
                    
            except Exception as e:
                print(f"❌ Fout in agent loop: {e}")
                break
        
        print("\n✅ Agent analyse voltooid!")

if __name__ == "__main__":
    agent = VlaamseCodexAgent()
    agent.voer_uit() 