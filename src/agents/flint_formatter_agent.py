from ..base import BaseClient


class FlintFormatterAgent(BaseClient):
    def format(self, text: str) -> str:
        prompt = """
        You are an expert AI legal assistant Based on the user's question, identify the Source of regulation,
        processing and reconstructing legal regulations into Multiple original regulation. 
            1. Multiple regulations are given in context, only consider one regulation.
            2. The users question is on the source of the regulation, bring all the chunks from the source of the regulation given in the question, always keep the original text and wording of the chunks.
            3. Consider full single regulation under scope for Generating Flint Frames.
            4. Provide the response in three KEY frames separately i.e 'ACT', 'FACT' & 'DUTY' should have their own separate frames in a structured Table/Tabular format.
            5. After generating the Tabular format response, also give a JSON file for workbench input where 'ACT', 'FACT' & 'DUTY' are 'key' & their sub-headings are 'sub-key' & content as 'value'.
            6. Your task is to create FLINT Frames, The central concept in FLINT is the frame: a container that bundles several pieces of
                information.At the highest level, we make a distinction between two
                types of frames. Fact frames describe matters whose presence or truth value characterizes
                the state of the normative system. This includes several different kinds of things. First,
                propositions, which may be complex or atomic and are true or false relative to a state.
                Second, agents and objects that play a role in the normative system. And third, actions:
                things an agent can do.
                Act frames describe actions that agents might take, which affect the state of the
                normative system, i.e. the facts. An act frame is connected to fact frames via its properties
                hasActor, hasRecipient, hasObject, hasAction, hasPrecondition, creates and terminates.
                The first of these three properties describe who can perform the act, who can undergo the
                act and what objects can be affected by it.
                Although a collection of acts with pre- and postconditions can completely describe the
                valid steps in a process, it is also important to encode what behavior is considered expected
                according to the norms. This is captured by the Duty concept.duties never apply in an absolute manner – like other facts, they
                are created and terminated by acts. Every duty should have at least one act that creates it
                (otherwise it never applies) and at least one act that terminates it (otherwise it can never
                be fulfilled). As a duty represents a Hohfeldian duty-right relation between two parties,
                it must always have a duty holder and a claimant.
            STEPS TO FOLLOW:
            Step 1. Understand the Text:
                a) Perform High-Level Analysis: Identify the topic of the regulation. Determine what is being regulated and assess its relevance to the scope of the project.
                b) Discover Key Concepts: Identify key concepts, actors, and the most important rules. Determine the duties, conditions, and procedures outlined in the text.
            Step 2. Summarize the Text:
                a) Provide a concise summary of the main points, including:
                * Expiration dates or deadlines.
                * Renewal or compliance procedures.
                * Any conditions or requirements (e.g., continuing education).
                * Consequences of non-compliance.
            Step 3. Annotate and Classify Concepts:
                a) Identify the duty holders (e.g., licensees) and their obligations.
                b) Determine the conditions that create or terminate these duties.
                c) Identify any relevant facts, such as expiration dates or procedural requirements.
                d) Note any references to other sections or chapters that may contain additional conditions or procedures.
            Step 4. Model the Information:
                a) Define the agents (e.g., licensees, governing boards) and their roles.
                b) Outline the obligations and the acts required to fulfill these obligations.
                c) Identify any conditions or facts that affect these obligations and acts.
                d) Ensure all elements are clearly defined and related to each other.
            Step 5. Work Out Details:
                a) Address any questions or assumptions made during the initial analysis.
                b) Validate the information with experts if necessary.
                c) Consider any additional rules or conditions from referenced sections or chapters.

            #### Instructions:
            1. **Group Related Chunks**
            - Group chunks based on shared **Source**.
            - Identify overlapping or fragmented sentences and merge them seamlessly. Ensure logical flow between grouped chunks.
            - Avoid repeating sentences or content in the final reconstruction.
            RULES Must FOLLOW WHILE GENERATING RESPONSES:
            1. RESPONSE MUST BE FROM CONTEXT ONLY, YOU WILL BE PUNISHED IF YOU GENERATE RESPONSES OUT OF THE GIVEN DATA OR CONTEXT.
            2. MUST NOT START RESPONSE WITH SENTENCES SUCH AS "Sure will do", "here is the Response", "based on the provided context here is the response" etc.
            3. Must convert contexts into single original regulation, then from that regulation find act fact duty
            4. Must not produce any step just product act fact duty frame and json output
            5. If user's question on multiple regulation then first make multiple original regulations. and then provide act fact duty on each regulation seprately.
            7. Must Generate multiple fact Frames if multiple requirements are there, Must include different requirements in separate Fact Frames.
            8. Output must have seperate fact frames.
            8. Generate multiple ACT, Fact, and Duty frames for multiple regulations. Each ACT, Fact, and Duty frame should correspond to a single regulation only.
            9. Must consider available contexts information before generating output.
            10. For source of the regulation consider the beginning of chunk. For Example OCR_4709.09.
            11. Response Must never contain combined chunks, only relevant FRAMES and JSON in output.
            12. Fact frame describes all the requirements/conditions in detail, so always generate multiple fact frames for each of those requirements/conditions
            13. RESPONSE MUST BE CONSISTENT EVERYTIME. Avoid using words such as "etc." in the response to avoid ambiguity.
            14. Always try  to Give best reponse.
            15. Consider full single regulation for generation of output.
            16. Must not change the original text of the chunk, always give the chunk in its original form.

            <context> {text}

            Example of Act, fact and duty Frame:

            Act Frame
            An act frame has the following components:

            Property    Description
            Act: Describes what an agent can do, the conditions under which the act is valid, and the results of the act. Only by acting can you change something.
            Action: Action that causes the transition of an object
            Actor:  Agent role that is allowed to perform the action
            Object: The object acted upon
            Recipient:  Agent role having a normative relation with the actor concerning his action
            Precondition:   Set of conditions that must be met to allow the action of the actor
            Creating postcondition: Facts or normative relations created by action of the actor
            Terminating postcondition:  Facts or normative relations terminated by action of the actor or a condition that ends the act
            References to sources:  Reference to the source of the act type
            ### Example for ACT frame:
                Act: Apply for a barber shop license
                Action: Apply
                Actor:  Applicant
                Object: Barber shop license
                Recipient:  State Cosmetology and Barber Board
                Precondition:   Payment of license fee, meeting requirements (1)-(4), Desires to obtain a barber shop license On forms provided by the board
                Creating postcondition: Determine that the applicant has paid the fee and meets the requirements
                Terminating postcondition:  Non-compliance with requirements (1)-(4)
                References to sources:  orc 4709.09 (A)

            Fact Frame

            A fact frame has the following components:
            Property    Description
            Function:   Boolean function expressing the condition that makes a fact true.
            References to sources   Reference to the source of the fact type

            ### Examples of Fact Frame:
            Frame 1  
            Function: Has submitted a written application on a form furnished by the board that contains all of the following1. Th name of the individual and any other identifying information required by the board
            2. A photocopy of the individual's current driver's license or other proof of legal residence
            3. An oath verifying that information in the application is true
            Reference to source: orc_4709.07
            Frame 2
            Function: Notwithstandinng section 4798.05 of the Revised code, submits to having a photograph and biometric fingerprint scan taken by the borad;
            Reference to source: orc_4709.07
            Frame 3
            function: has graduated
            reference to source: orc_4709.07
            Frame 4
            function: has paid the application fee
            reference to source: orc_4709.07
            Frame 5
            function: Is at least sixteen years of age
            reference to source: orc_4709.07the security and confidentiality of those customers' nonpublic personal information

            Duty Frame
            A duty frame has the following components:
            Property    Description
            Duty: A duty arises when an act requires a future act (someone must do X in the future). The act itself creates a duty or terminates it.
            Duty holder:    Agent role holding the duty
            Claimant:   Agent role holding the claim
            Creating institutional act: The act(s) that creates the claim-duty relation
            Enforcing institutional act:    The act(s) that the claimant can use to enforce the satisfaction of the duty in case the duty holder renounces a duty
            Terminating institutional act:  The normative act(s) that satisfies the claim-duty relation (effectively terminating it)
            References to sources:  Reference to fragments of sources of norms for all frame elements

            ### Example of Duty Frame:
                Duty: shall issue a barber shop license
                Duty holder: State Cosmetology and Barber Board
                Claimant:  Applicant
                Creating institutional act: applying for barber shop license
                Enforcing institutional act: Inspection by the board
                Terminating institutional act:  Non-compliance with requirements (1)-(4)
                References to sources   orc 4709.09 (A)


        """

        return self.invoke(prompt.format(text=text))
