# Europarl-ST Data Card
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [Europarl-ST website](https://www.mllp.upv.es/europarl-st/)  |Download the dataset|

## Preprocessing Principles

You may refer to [preprocess_Europarl-st.py](/data_preprocess/preprocess_Europarl-st.py) for all the details. Here is a concise summary:

The dataset contains audio and transcriptions of 9 different languages. It is first divided by the 9 languages. Inside each language, there is a folder with the audios and 8 different folders from the remaining 8 languages. Each folder contains: 

- **`segments.source_language`** A text file containing for each line a transcription in the original language.
- **`segments.destination_language`** A text file containing for each line a transcription in the translated language.
- **`segments.lst`** A text file containing for each line the timestamps.

We create a json file with the transcription in the text field but we also include the translations. 

####
```json
{
   "text":[
      "A person is saying: \"I ask for your support to ensure that we have confident, well-informed consumers for electronic communications, who are also secure and know that their personal data is protected.\""
   ],
   "tag":[
      "Speech",
      "Politician",
      "Parliament"
   ],
   "original data":{
      "title":"Europarl-ST Dataset",
      "description":"Europarl-ST is a Multilingual Speech Translation Corpus, that contains paired audio-text samples for Speech Translation, constructed using the debates carried out in the European Parliament in the period between 2008 and 2012.",
      "transcriptions":{
         "es":"Solicito su apoyo para asegurar que tenemos consumidores de comunicaciones el\u00e9ctronicas confiados y bien informados, que tambi\u00e9n est\u00e1n seguros y saben que sus datos personales est\u00e1n protegidos.",
         "de":"Ich bitte Sie um Ihre Unterst\u00fctzung, um sicherzustellen, dass die Verbraucher gut informiert sind und Vertrauen in die elektronische Kommunikation haben, dass sie auch sicher sind und wissen, dass ihre personenbezogenen Daten gesch\u00fctzt sind.",
         "en":"I ask for your support to ensure that we have confident, well-informed consumers for electronic communications, who are also secure and know that their personal data is protected.",
         "fr":"J'en appelle \u00e0 votre soutien pour faire en sorte que les consommateurs soient confiants et bien inform\u00e9s face aux communications \u00e9lectroniques, pour qu'ils aient la s\u00e9curit\u00e9 et que leurs donn\u00e9es personnelles soient prot\u00e9g\u00e9es.",
         "nl":"Ik vraag u nu om uw steun, zodat we kunnen zorgen voor goed voorgelichte consumenten die vertrouwen hebben in elektronische communicatie en die bovendien goed zijn beveiligd en weten dat hun persoonsgegevens worden beschermd.",
         "pl":"Prosz\u0119 o pa\u0144stwa wsparcie celem zapewnienia, by\u015bmy mieli pewnych swych praw, dobrze poinformowanych konsument\u00f3w narz\u0119dzi \u0142\u0105czno\u015bci elektronicznej, bezpiecznych i \u015bwiadomych ochrony i danych osobowych.",
         "pt":"Pe\u00e7o o vosso apoio para assegurar que teremos consumidores confiantes e bem informados no dom\u00ednio das comunica\u00e7\u00f5es electr\u00f3nicas, e tamb\u00e9m para que eles se sintam seguros e saibam que os seus dados pessoais est\u00e3o protegidos.",
         "ro":null,
         "it":"Chiedo il vostro sostegno per far s\u00ec che i consumatori possano avere fiducia ed essere ben informati in materia di comunicazione elettronica, oltre ad essere consapevoli e sicuri che i loro dati personali saranno tutelati."
      }
   }
}
```
      
```json
{
   "text":[
      "Una persona esta diciendo: \"Se\u00f1or Presidente, simplemente quisi\u00e9ramos, desde mi Grupo, poner de manifiesto que el actual marco presupuestario y financiero de 2007 a 2013 dificulta mucho que se puedan dar respuestas eficaces a las nuevas prioridades pol\u00edticas.\""
   ],
   "tag":[
      "Speech",
      "Politician",
      "Parliament"
   ],
   "original data":{
      "title":"Europarl-ST Dataset",
      "description":"Europarl-ST is a Multilingual Speech Translation Corpus, that contains paired audio-text samples for Speech Translation, constructed using the debates carried out in the European Parliament in the period between 2008 and 2012.",
      "transcriptions":{
         "es":"Se\u00f1or Presidente, simplemente quisi\u00e9ramos, desde mi Grupo, poner de manifiesto que el actual marco presupuestario y financiero de 2007 a 2013 dificulta mucho que se puedan dar respuestas eficaces a las nuevas prioridades pol\u00edticas.",
         "de":"Herr Pr\u00e4sident! Meine Fraktion m\u00f6chte nur deutlich machen, dass es aufgrund des derzeitigen Haushalts- und Finanzrahmens f\u00fcr 2007 bis 2013 sehr schwierig ist, wirksam auf die neuen politischen Priorit\u00e4ten zu reagieren.",
         "en":"Mr President, my Group simply wants to highlight that the current budgetary and financial framework for 2007 to 2013 makes it very difficult to respond effectively to the new political priorities.",
         "fr":"Monsieur le Pr\u00e9sident, mon groupe tient tout simplement \u00e0 souligner le fait que le cadre budg\u00e9taire et financier actuel pour la p\u00e9riode 2007-2013 permet tr\u00e8s difficilement de r\u00e9agir efficacement aux nouvelles priorit\u00e9s politiques.",
         "nl":"Mijnheer de Voorzitter, mijn fractie wil alleen maar benadrukken dat het met het huidige financieel begrotingskader 2007-2013 zeer moeilijk is om doeltreffend op de nieuwe politieke prioriteiten te reageren.",
         "pl":"Panie przewodnicz\u0105cy! Moja grupa pragnie jedynie podkre\u015bli\u0107, \u017ce obecne ramy bud\u017cetowe i finansowe na lata 2007 \u2013 2013 bardzo utrudniaj\u0105 skuteczne dzia\u0142anie w obliczu nowych priorytet\u00f3w politycznych.",
         "pt":"Senhor Presidente, o meu grupo pretende simplesmente sublinhar que o actual quadro or\u00e7amental e financeiro para o per\u00edodo de 2007 a 2013 torna muito dif\u00edcil responder eficazmente \u00e0s novas prioridades pol\u00edticas.",
         "ro":null,
         "it":null
      }
   }
}
```
### I. Json file generation principles 
-  **` text  entry`**  We include in the 9 different languages a text with the following structure: `A person is saying: "ORIGINAL TRANSCRIPTION"`.

- **`tag  entry`** Speech, Politician, Parliament.
- **`Original_data`** We include a `translations  entry` with the text translated to the other languages.  
### II. Audio filtering principles
1. Keep samples no longer than **3** minutes, and discard the rest.
2. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
3. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).