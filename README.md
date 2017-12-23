# Iris
School final project / עבודת גמר

DISCLAIMER: 
NOT DONE, STILL WORKING ON IT, NOT EVERYTHING IS IMPLEMENTED YET.

This is a project I am doing as an extra credit for school.
The project is about personal assistant's and how computers understand us, 
It is my first project to be written in python so please excuse me.

The pyhon server recives querys from clients (will be written in java) and handles them in threads.
It uses stanford's amazing Core-NLP to parse the text, The parsed text is ran in a rule based algorithm that decideds whatever it is a question or not,
If it is a question it tries to find what kind of question it is (from its json rule file).
If it does not know how to answer a query, it will do what siri does and choose the easy way out, AKA google search it.
