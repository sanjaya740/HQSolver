HQSolver
========

An tool for predicting correct answers in HQ Trivia!
----------------------------------------------------

Disclaimers
------------

- This project is (and was created) for educational purposes only!
- This tool wasn't created for helping people win HQ Trivia!

Requirements
------------

Library            | Version
------------------:|:---------
Python             | 3.6
autobahn           | 17.10.1 or later
Google-Search-API  | 1.1.14 or later
nltk               | 3.2.5 or later
service_identity   | 17.0.0 or later
requests           | 2.18.4 or later
Twisted            | 17.9.0 or later
wikipedia          | 1.4.0 or later

***...or just install all dependenties via pip (`pip -r requirements.txt`)***

Installation
------------

- Install Python and all required dependencies (see above)
- Paste needed keys in `config.ini`
- Configure this to your preferences (see below)

Configuration
-------------

****NOTE: Enable/Disable options MUST have one of the following values `True` or `False`****

- API: As you can see in section description in `config.ini` do not touch it if you don't know what are you doing. DO NOT
    - `shows_now` - url to api request to get show status/info
- Chat: Chat options
    - `enable` - Enable/Disable chat feature
    - `show_kicked` - Enable/Disable informing when somebody was kicked from chat
    - `show_message` - Enable/Disable showing chat message
    - `show_userids` - Enable/Disable showing User IDs
    - `show_usernames` - Enable/Disable showing Usernames
- GameSummary: End of the game (when winners are shows) options
    - `enable` - Enable/Disable showing game summary
    - `show_prize` - Enable/Disable showing how much user won
    - `show_userids` - Enable/Disable showing User IDs
    - `show_usernames` - Enable/Disable showing Usernames
- General: General settings
    - `debug_mode` - Enable/Disable special debug messages
    - `hq_client` - Your HQ Client (usally OS/Version)
    - `server_ip` - API server for HQ Trivia (in case if they change it)
- Login: Login details
    - `authorization_key` - Your authorization key grabbed from game client
- Solver: Solver options
    - `google_api_key` - Your Google API Key
    - `google_cse_id` - Your Google Custom Search Engine ID
    - `show_advancing_players` - Enable/Disable showing how many players passed question (in total)
    - `show_answers` - Enable/Disable showing answers
    - `show_answersids` - Enable/Disable showing answers IDs
    - `show_category` - Enable/Disable showing question category
    - `show_eliminated_players` - Enable/Disable showing how much players was eliminated (in total)
    - `show_summary` - Enable/Disable showing Question Summary
    - `show_players_answers` - Enable/Disable showing how many players tapped specified answer
    - `show_question` - Enable/Disable showing question
    - `show_questionids` - Enable/Disable showing question IDs
    - `show_question_count` - Enable/Disable showing how many questions are in current show
    - `show_question_number` - Enable/Disable showing which question is it
    - `use_naive` - Enable/Disable Naive solver
    - `use_google` - Enable/Disable Google solver
    - `use_wiki` - Enable/Disable Wikipedia solver

How to run?
-----------

- Run `main.py` while game is active
- That's it!

FAQ (Frequently Asked Questions)
--------------------------------

- Q: This solver just gave me wrong answer!
- A: As you can see in the description, it's an tool for "predicting" answers. So please don't expect 100% accuracy.

- Q: How to get authorization key?
- A: This key can be found by sniffing the traffic on your phone. 

- Q: Where to get Google API key and Custom Search Engine ID?
- A: https://developers.google.com/custom-search/json-api/v1/overview#prerequisites

- Q: I found a bug, where to report it?
- A: In the Issues tab (please also include log/screenshot or something)

- Q: I want to help you with this project! Can I?
- A: Of course! Any help are highly appreciated!


Solvers Info
------------

****NOTE: All solvers logic are in `solvers` folder****

Solver Name  | File         | Short description
------------:|:------------:|:--------------------------------------------------------------------------------------------------------------
Naive        | `naive.py`   | Uses Google CSE API, checks how many times the answers appear on the results page
Google       | `gsearch.py` | Similar to Naive, but doesn't need CSE API, and it uses more advanced techniques for predicting answers
Wikipedia    | `wiki.py`    | Searches wikipedia for words that are in answers, if these pages exists, checks the probability of that answer


Credits
-------

****Main programmer/Developer****
- Marek Grzyb (B1naryKill3r)
