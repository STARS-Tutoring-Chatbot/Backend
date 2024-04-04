from fastapi import APIRouter, Request
from langchain.llms import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    SemanticSimilarityExampleSelector,
)
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import openai
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path)

api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")
jwt_secret = os.getenv("JWT_SECRET")
openai_api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

# Define your examples
examples = [
    {
        "input": "What is a loop in Python?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: What is a loop in Python?
So the final answer is: In Python, a loop is a way to iterate over a sequence (like a list or tuple) or other iterable objects. The most common types of loops in Python are the 'for' loop and the 'while' loop. Would you like to see an example or review the concept of loops in more detail?
"""
    },
    {
        "input": "Write a function in Python that reverses a string.",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: Yes.
Follow up: What concepts are needed to complete the following: Write a function in Python that reverses a string.
So the final answer is: Instead of providing a complete solution, let's review some concepts that will help you write the function: string manipulation in Python, writing functions in Python. Which concept would you like to start with?
"""
    },
    {
        "input": "I'm getting a error with this Python code: for i in range(10) print(i)",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: I'm getting a error with this Python code: for i in range(10) print(i)
So the final answer is: It looks like you're missing a colon after the 'range(10)' in your 'for' loop. The correct syntax should be: for i in range(10): print(i). The colon is used to indicate the start of the loop's body. Would you like to review the syntax of 'for' loops in more detail?
"""
    },
    {
        "input": "What is polymorphism in Java?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: What is polymorphism in Java?
So the final answer is: Polymorphism in Java is the ability of an object to take on many forms. It allows one interface to be used for a general class of actions. The most common use of polymorphism in OOP is when a parent class reference is used to refer to a child class object. Would you like to explore an example of polymorphism or review the concept in more detail?
"""
    },
    {
        "input": "Can you solve this assignment for me? Write a function in Python that reverses a string.",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: Yes.
Follow up: What concepts are needed to complete the following: Write a function in Python that reverses a string.
So the final answer is: Instead of providing a complete solution, let's review some concepts that will help you write the function: string manipulation in Python, writing functions in Python. Which concept would you like to start with?
"""
    },
    {
        "input": "My Python loop isn't working as expected. Can you help me debug it? for i in range(10): print(i)",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: My Python loop isn't working as expected. Can you help me debug it? for i in range(10): print(i)
So the final answer is: It looks like your loop is syntactically correct, but if it's not working as expected, you might want to check the following: Ensure that the range is correct for the desired output. Check if there are any conditions or additional code inside the loop that could affect its behavior. You might want to review the concept of loops in Python and debugging techniques. Would you like to go over some debugging tips or review loops?
"""
    },
    {
        "input": "I'm getting a syntax error with this Python code: for i in range(10) print(i)",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: I'm getting a syntax error with this Python code: for i in range(10) print(i)
So the final answer is: It looks like you're missing a colon after the 'range(10)' in your 'for' loop. The correct syntax should be: for i in range(10): print(i). The colon is used to indicate the start of the loop's body. Would you like to review the syntax of 'for' loops in more detail?
"""
    },
    {
        "input": "My function isn't returning the right result. def add(a, b): return a * b",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: My function isn't returning the right result. def add(a, b): return a * b
So the final answer is: It seems like your function is multiplying 'a' and 'b' instead of adding them. To fix this, you should use the '+' operator instead of '*'. Here's the corrected function: def add(a, b): return a + b. You might want to review the concepts of functions and operators in Python. Would you like to go over these concepts?
"""
    },
    {
        "input": "I'm getting a 'NameError: name 'x' is not defined' in Python. What does this mean?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: No.
Follow up: I'm getting a 'NameError: name 'x' is not defined' in Python. What does this mean?
So the final answer is: A 'NameError' in Python indicates that the interpreter couldn't find a variable or function with the specified name. In this case, 'x' is not defined before it's being used. To fix this, you should ensure that 'x' is defined before using it, or check for typos in the variable name. Would you like to review variable scope and declaration in Python?
"""
    },
    {
        "input": "I need to write a Java method called 'triangle' that prints a pattern of asterisks, where the number of asterisks increases from m to n and then decreases back to m. How can I do this using recursion?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: Yes.
Follow up: What concepts are needed to complete the following: I need to write a Java method called 'triangle' that prints a pattern of asterisks, where the number of asterisks increases from m to n and then decreases back to m. How can I do this using recursion?
So the final answer is: It sounds like you're working on a recursive method in Java. To approach the 'triangle' method, consider how the pattern changes with each recursive call. You'll need a base case when m equals n, and for each recursive step, you can increase or decrease the number of asterisks. Think about how you can modify the parameters in the recursive call to reflect this pattern. Would you like to go over the concept of recursion and base cases in more detail?
"""
    },
    {
        "input": "I need to implement a recursive method in Java to print section numbers with a given prefix and levels. How should I approach this?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: Yes.
Follow up: What concepts are needed to complete the following: I need to implement a recursive method in Java to print section numbers with a given prefix and levels. How should I approach this?
So the final answer is: For the section numbers problem, you'll need to use recursion to generate the numbers with the specified levels. Consider how you can concatenate the prefix with the current level number and pass it to the next recursive call. You'll also need a base case to stop the recursion when you reach the desired level. Here's some pseudocode to get you started: public static void printSections(String prefix, int level) { if (level == 0) { System.out.println(prefix); return; } for (int i = 1; i <= 9; i++) { printSections(prefix + i + '.', level - 1); } }. This pseudocode outlines the structure of the recursive method. You'll need to adapt it to fit the specific requirements of your assignment. Would you like to review any concepts related to string manipulation or recursion?
"""
    },
    {
        "input": "How can I create a recursive function in Java to reverse a string?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: Yes.
Follow up: What concepts are needed to complete the following: How can I create a recursive function in Java to reverse a string?
So the final answer is: To create a recursive function for reversing a string in Java, you'll need to think about the base case and the recursive step. The base case could be when the string is empty or has a single character. For the recursive step, you can concatenate the last character of the string with the result of the recursive call on the substring excluding the last character. Here's some pseudocode to illustrate this: public static String reverseString(String str) { if (str.length() <= 1) { return str; } return str.charAt(str.length() - 1) + reverseString(str.substring(0, str.length() - 1)); }. This pseudocode provides a basic structure for the recursive function. You'll need to refine it and ensure it meets the requirements of your assignment. Would you like to go over the concepts of string manipulation and recursion in more detail?
"""
    },
    {
        "input": "I'm struggling with writing a recursive method to calculate the factorial of a number in Java. Any tips?",
        "output": """
Are follow up questions needed here: Yes.
Follow up: Does this response do the assignment for you?
Intermediate answer: Yes.
Follow up: What concepts are needed to complete the following: I'm struggling with writing a recursive method to calculate the factorial of a number in Java. Any tips?
So the final answer is: For writing a recursive method to calculate the factorial of a number in Java, you'll need to define a base case and a recursive case. The base case is usually when the number is 0 or 1, and the recursive case involves calling the method with the number minus one. Here's some pseudocode to help you get started: public static int factorial(int n) { if (n <= 1) { return 1; } return n * factorial(n - 1); }. This pseudocode outlines the basic structure of the recursive method. Remember to test your method with different input values to ensure it's working correctly. Would you like to review the concept of recursion or how to handle base cases in recursive methods?
"""
    },
]

# Create the vector store
to_vectorize = [" ".join(example.values()) for example in examples]
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

# Create the example selector
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore, k=2
)

# Define the few-shot prompt template
few_shot_prompt = FewShotChatMessagePromptTemplate(
    input_variables=["input"],
    example_selector=example_selector,
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

# Assemble the final prompt template
final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a college level computer science tutor that helps students understand concepts. However, you do not solve assignments for students, or write code for them. You only assist them with learning concepts and debugging.",
        ),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

# Use OpenAI's GPT-4 model for the chat agent
chat_model = ChatOpenAI(model="gpt-4", temperature=0.0, openai_api_key=openai_api_key)

# Define the parser
parser = PydanticOutputParser(pydantic_object=ListOfCodeBlocks)

# Create the chain with the final prompt, the chat model, and the parser
chain = final_prompt | chat_model | parser


@router.post("/api/extractor/test/people")
async def postOpenAIExtractor(request: Request):
    request_body = await request.json()
    query = request_body["data"]

    res = chain.invoke({"input": query})

    return {
        "Type": "test",
        "query": request_body,
        "result": res,
    }


@router.post("/api/extractor/test/isCamelCase")
async def isCamelCase(request: Request):
    request_body = await request.json()
    query = request_body["data"]

    res = chain.invoke({"input": query})

    return {
        "Type": "test",
        "query": request_body,
        "result": res,
    }
