import string
import yaml
from .prompt_template_unit  import PromptTemplateUnit

# from indented_logger import IndentedLogger
# import logging
# logger_setup = IndentedLogger(name='prepromptbuilder', level=logging.INFO, include_func=True)

l= []

class Bin():
    def __init__(self):
        self.storage= []
        self.questinables=[]

    def add(self, thing):
        self.storage.append(thing)

    def reset(self):
        self.storage = []

    def bring(self, name):

        for p in self.storage:
            pass

        for idx, p in enumerate(self.storage):
            if  p.name == name:
                return p

    def bring_by_category(self, cat):
        selections=[]
        for idx, p in enumerate(self.storage):
            if p.category == cat:
                selections.append(p)
        return  selections
    def find_questionable_prompts(self):
        questinables=[]
        for idx, p in enumerate(self.storage):
            if p.category=="context_prompts":
               # question = p
                questinables.append(p)

        self.questinables= questinables



class Proteas:
    def __init__(self, yaml_path=None, logger=None):
        """Initialize the PromptManager without any specific attributes."""
        self.bin= Bin()
        self.unit_objects=[]


        # self.logger = logger if logger else logger_setup.get_logger()
        self.logger =logger

        if yaml_path:
            self.load_unit_skeletons_from_yaml(yaml_path)

    def load_yaml_file(self,file_path):
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)  # Load the YAML data
        return yaml_data

    def bring(self, name):

        for idx, p in enumerate(self.unit_objects):
            if p.name == name:
                return p


    def bring_by_category(self, cat):
        selections=[]
        for idx, p in enumerate(self.unit_objects):
            if p.category == cat:
                selections.append(p)
        return  selections


    def load_unit_skeletons_from_yaml(self, yaml_file_path):

        yaml_data = self.load_yaml_file(yaml_file_path)
        self.unit_objects = self.create_units_from_skeletons(yaml_data)
        print( len(self.unit_objects), "prompt template units loaded")

    def bring_units(self, list_of_unit_names):
        p = []

        prompt_object_names=[p.name for p in self.unit_objects]
       # self.logger.info("prompt_object names: %s ", prompt_object_names, lvl=12)
        for name in list_of_unit_names:
            #self.logger.info("prompt name: %s ", name, lvl=13)
            r = self.bring(name)
            if not r:
                raise Exception(f"Unit with name:  '{name}' not found.")
            p.append(r)
        return p


    def is_list_of_strings(self, lst):
        return isinstance(lst, list) and all(isinstance(item, str) for item in lst)


    def add_units_to_bin(self, list_of_unit_names):
       # self.logger.info("list_of_preprompts: %s ", list_of_preprompts, lvl=12)
        if self.is_list_of_strings(list_of_unit_names):
            list_of_unit_names = self.bring_units(list_of_unit_names)

        for e in list_of_unit_names:
            self.bin.add(e)

    def craft(self, units, placeholder_dict=None):
        if units:
            self.add_units_to_bin(units)
        template_block = self.merge_simple(self.bin.storage, placeholder_dict)
        # prompt_template_block
        self.bin.reset()
        return template_block

    def merge_simple(self, unit_objects, placeholder_dict=None):

        template_block = ""
        unit_objects_constructed = [prompt.construct_statement() for prompt in unit_objects]

        formatter = string.Formatter()

        # Dynamically build the unformatted prompt using the constructed informative pieces
        for piece in unit_objects_constructed:
            # Extract the field names from the piece using the string formatter
            field_names = [field_name for _, field_name, _, _ in formatter.parse(piece) if field_name]
            if placeholder_dict:
                if all(placeholder_dict.get(field) is not None for field in field_names):
                    try:
                        template_block += f"{piece}\n"
                    except KeyError:
                        # Skip this piece if the key isn't present in placeholder_dict
                        continue
            else:
                template_block += f"{piece}\n"

        return template_block


    def add_all_units_to_bin(self):
        self.bin.storage=  self.unit_objects

    def add_to_bin(self, p):
        self.bin.add(p)

    # def generate_content(self, command_prompt,  context_data):
    #
    #     final_preprompt=self.arrange_prompts(self.bin.storage, context_data)

    def find_candidate_question(self,questinables, also_not_answered_before =False):
        # for e in questinables:
        #     # if e.marked_as_question:
        #         # print(marked_as_question)
        #         if also_not_answered_before:
        #             if not e.answered:
        #                 return e
        #         else:
        #             return e

        for e in questinables:
                if not e.answered:
                    return e


    def craft_question_using_category(self, data_for_placeholders,  question_category, supporter_category=None):

        #self.logger.info(" >>>>>>>>>  question_category  %s ", question_category, lvl=12)
        questinables=self.bin.bring_by_category( question_category)

        merged_string = ", ".join(obj.name for obj in questinables)
        #self.logger.info(">>>>>>>>>   questinables  %s ", merged_string, lvl=12)

        question= self.find_candidate_question( questinables, also_not_answered_before=True)

        #self.logger.info(" >>>>>>>>> type(question)   %s ", type(question), lvl=12)
        # self.logger.info(" >>>>>>>>> question name  %s ",question.name , lvl=12)
        question.make_question()
        question_constructed = question.construct_statement()

        # Remove the question prompt from the list to only have the informative prompts remaining
        deactive_questinables = [unit for unit in questinables if unit != question]
        # deactive_questinables_constructed = [prompt.construct_statement() for prompt in deactive_questinables]

        # prompt = ""
        template_block= ""
        if supporter_category:
            supporter_category_units = self.bin.bring_by_category(supporter_category)

            supporter_category_units_constructed = [unit.construct_statement() for unit in supporter_category_units]
            for e in supporter_category_units_constructed:
                template_block += f"{e}\n\n"

        # prompt = f"{question_constructed}\n\n"

        template_block += self.merge_simple(deactive_questinables, data_for_placeholders)

        template_block += f"{question_constructed}\n\n"

        question.close_question()

        #prompt += self.build_informative_prompt(informative_prompts_constructed, context_data)

        return template_block, question

        # informative_prompts = [prompt for prompt in prompt_objects if prompt.category != "command_prompts"]


    def dynamic_prompt_maker(self, prompt_name, prompt_text):

        unit_object = PromptTemplateUnit(
            name=prompt_name,
            info=prompt_text,
            category="dynamic"
        )

        self.unit_objects.append(unit_object)


    def create_units_from_skeletons(self, yaml_data):
        """
        Create PromptObject instances from YAML data.
        Assign 'info' as usual, and set 'purpose' based on the main key (e.g., 'meta_prompts' or 'context_prompts').
        :param yaml_data: The full YAML data for the prompts.
        """
        unit_objects = []

        # Loop through the main keys (e.g., 'meta_prompts', 'context_prompts')
        for category, data in yaml_data.items():
            for unit_data in data:
                prompt_object = PromptTemplateUnit(
                    name=unit_data["name"],
                    statement_suffix= unit_data.get("statement_suffix", "") ,  # Assign 'self.statement_suffix'
                    placeholder_proclamation= unit_data.get("placeholder_proclamation", None) ,
                    placeholder= unit_data.get("placeholder", None) ,
                    info=unit_data.get("info", None),
                    category=category
                )
                unit_objects.append(prompt_object)

        return unit_objects


    def build_informative_template_block(self, informative_units_constructed, context_data):
        """
        Build the informative part of the prompt using the constructed informative pieces and context data.
        :param informative_prompts_constructed: List of constructed informative prompts.
        :param context_data: Dictionary with context data for filling the placeholders.
        :return: Unformatted informative part of the prompt as a string (placeholders remain intact).
        """
        template_block = ""
        formatter = string.Formatter()

        # Dynamically build the unformatted prompt using the constructed informative pieces
        for piece in informative_units_constructed:
            # Extract the field names from the piece using the string formatter
            field_names = [field_name for _, field_name, _, _ in formatter.parse(piece) if field_name]

            if all(context_data.get(field) is not None for field in field_names):
                try:
                    # Format the piece with the available context data
                    template_block += f"{piece}\n\n"
                except KeyError:
                    # Skip this piece if the key isn't present in context_data
                    continue

            # Check if all fields in the piece have non-None values in context_data
            # In this case, we're skipping formatting and preserving the unformatted pieces
            # prompt += f"{piece}\n\n"

        return template_block

    def merge_by_category(self, category, context_data, filter_list=None):
        unit_objects = self.bin.storage

       # print("merge_by_category---------------------------")

        # print("category  ", category)
        # print("len(prompt_objects )  ", len(prompt_objects ))

        if not isinstance(category, list):
            category = [category]
        if not isinstance(filter_list, list):
            filter_list = [filter_list]

        # same_category_prompt_objects = [prompt for prompt in prompt_objects if prompt.category != category]
        same_category_unit_objects = [unit for unit in unit_objects if unit.category in category]


        if filter_list:
            filtered_same_category_unit_objects = [prompt for prompt in same_category_unit_objects if prompt.name not in filter_list]
        else:
            filtered_same_category_unit_objects = same_category_unit_objects
        #constructed_filtered_same_category_prompt_objects= [prompt.construct_statement() for prompt in filtered_same_category_prompt_objects]


        template_block = " "
        template_block +=self.merge_simple( filtered_same_category_unit_objects, placeholder_dict=context_data)

        # Use the new method to build the informative prompt part
       # prompt += self.build_informative_prompt(informative_prompts_constructed, context_data)

        return template_block

    def gather_informative(self,  context_data, filter_list=None, dont_bring_guide=False):
        unit_objects=self.bin.storage

        informative_units = [unit for unit in unit_objects if unit.category != "command_prompts"]
        informative_units = [unit for unit in informative_units if unit.name != "step_guide"]
        if filter_list:
            filtered_informative_units = [prompt for prompt in informative_units if prompt.name not in filter_list]
        else:
            filtered_informative_units=informative_units
        informative_units_constructed = [prompt.construct_statement() for prompt in filtered_informative_units]

        # Initialize the prompt with the question
        # prompt = f"{question_constructed}\n\n"

        template_block = " "

        # Use the new method to build the informative prompt part
        template_block += self.build_informative_template_block(informative_units_constructed, context_data)

        return template_block



    def arrange_units(self, unit_objects, context_data):
        """
        This method arranges the prompt objects, selecting the one that is in question form
        and constructing the rest to be used as informative context.
        :param prompt_objects: List of prompt objects
        :param context_data: Data to be passed into the prompts for context filling
        :return: The fully constructed prompt as a string.
        """
        question = None
        informative_units = []

        # Find the first prompt that is in question form
        for idx, p in enumerate(unit_objects):
            if p.marked_as_question:
                question = p
                break  # Once we find the question, stop the loop

        # If a question prompt was found
        if question:
            # Remove the question prompt from the list to only have the informative prompts remaining
            informative_units = [unit for unit in unit_objects if unit != question]

            informative_units = [unit for unit in unit_objects if unit.category != "command_prompts"]


            # Construct the question and informative prompts
            question_constructed = question.construct_statement()
            informative_units_constructed = [prompt.construct_statement() for prompt in informative_units]

            # Initialize the prompt with the question
            template_block = f"{question_constructed}\n\n"

            # Use the new method to build the informative prompt part
            template_block += self.build_informative_template_block(informative_units_constructed, context_data)

            return template_block

        # If no question prompt was found, return an empty string or some error indication
        return ""



    def create_prompt(self, question, units, context_data):
        """
        Create a prompt by stacking prompt pieces dynamically.
        :param question: The main question to ask.
        :param prompt_pieces: A list of strings with placeholders for dynamic content.
        :param context_data: A dictionary containing key-value pairs for formatting the placeholders.
        :return: A formatted prompt as a string.
        """
        # Start the prompt with the main question
        prompt = f"{question}\n\n"

        # Initialize a string formatter
        formatter = string.Formatter()

        # Dynamically build the prompt using the provided prompt pieces and context data
        for piece in units:
            # Extract the field names from the piece using the string formatter
            field_names = [field_name for _, field_name, _, _ in formatter.parse(piece) if field_name]

            # Check if all fields in the piece have non-None values in context_data
            if all(context_data.get(field) is not None for field in field_names):
                try:
                    # Format the piece with the available context data
                    formatted_piece = piece.format(**context_data)
                    prompt += f"{formatted_piece}\n\n"
                except KeyError:
                    # Skip this piece if the key isn't present in context_data
                    continue

        return prompt


def main():

    proteas = Proteas('prompts.yaml')

    order = ["business_documentation", "user_input", "answer_style"]

    filtered_data= { "business_documentation": "asdfjasdf",
                 "user_input": "userrrrsss",
                 "cccc" :" adsfasdf"
    }
    prompt_template_1 = proteas.craft(order)
    # template assembler based prompt orchestration
    # prompt_templating_system

    # from langchain_core.prompts import PromptTemplate
    from langchain.prompts import PromptTemplate

    prompt = PromptTemplate.from_template(prompt_template_1)
    formatted_prompt = prompt.format(**filtered_data)

    print(prompt_template_1)

    print("-------")

    print(formatted_prompt)



if __name__ == '__main__':
    main()
