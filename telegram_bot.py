import logging
from typing import Dict, Any

# Import detect_language function from utils
from utils import detect_language

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class KidQuestBot:
    def __init__(self):
        self.user_states: Dict[int, Dict[str, Any]] = {}
        
    async def start(self, update, context):
        """Send welcome message when /start command is issued."""
        user = update.effective_user
        user_id = user.id
        
        # Detect language from Telegram's built-in language_code if available
        detected_language = 'ru'  # Default to Russian
        telegram_language = "not detected"
        if user.language_code:
            # Check if the language code indicates English (en) or other supported languages
            lang_code = user.language_code.lower()
            if lang_code.startswith('en'):
                detected_language = 'en'
                telegram_language = "English"
            elif lang_code.startswith('ru'):
                telegram_language = "Russian"
        
        # Set initial state with language detection
        self.user_states[user_id] = {
            'quest_requirements': None,
            'current_quest': None,
            'current_step_id': None,
            'step_history': [],
            'quest_started': False,
            'user_language': detected_language
        }
        
        if detected_language == 'en':
            welcome_text = (
                "👋 Hello! I'm KidQuestBot - your assistant for creating "
                "wonderful text-based quests for children!\n\n"
                f"Your language preference: {telegram_language}\n\n"
                "Type /new to start a new quest!"
            )
        else:
            welcome_text = (
                "👋 Привет! Я KidQuestBot - твой помощник в создании "
                "восхитительных текстовых квестов для детей!\n\n"
                f"Ваш язык: {telegram_language}\n\n"
                "Напиши /new, чтобы начать новый квест!"
            )
        await update.message.reply_text(welcome_text)
        
    async def new_quest(self, update, context):
        """Initiate a new quest by asking for requirements."""
        user_id = update.effective_user.id
        user = update.effective_user
        
        # Clear any existing state for this user
        if user_id in self.user_states:
            del self.user_states[user_id]
            
        # Detect language from Telegram's built-in language_code if available, otherwise default to Russian
        detected_language = 'ru'  # Default to Russian
        if user.language_code:
            # Check if the language code indicates English (en)
            if user.language_code.startswith('en'):
                detected_language = 'en'
        
        # Set initial state with language detection
        self.user_states[user_id] = {
            'quest_requirements': None,
            'current_quest': None,
            'current_step_id': None,
            'step_history': [],
            'quest_started': False,
            'user_language': detected_language
        }
        
        if detected_language == 'en':
            welcome_text = (
                "🌟 Let's create a new quest together!\n\n"
                "Tell me about your quest: \n"
                "- Theme (e.g., adventures in the forest, underwater life, space travel)\n"
                "- Main character (e.g., little dragon, smart squirrel, robot explorer)\n"
                "- Educational element (e.g., learning animals, basic math, natural phenomena)\n"
                "- How many steps should be in the quest?\n\n"
                "Write freely - I'll make a great story from it!"
            )
        else:
            welcome_text = (
                "🌟 Давай создадим вместе новый квест!\n\n"
                "Расскажи мне, о чём будет твой квест: \n"
                "- Тема (например: приключения в лесу, подводная жизнь, космическое путешествие)\n"
                "- Главный герой (например: маленький дракон, умная белка, робот-исследователь)\n"
                "- Образовательный элемент (например: изучение животных, основы математики, природные явления)\n"
                "- Сколько шагов должно быть в квесте?\n\n"
                "Пиши всё свободным текстом - я сделаю из этого отличную историю!"
            )
        
        await update.message.reply_text(welcome_text)
        
    async def handle_requirements(self, update, context):
        """Handle user's requirements description for the quest."""
        user_id = update.effective_user.id
        user = update.effective_user
        
        if user_id not in self.user_states:
            # If no state exists, start a new quest
            await self.new_quest(update, context)
            return
            
        # Check if we already have requirements
        if self.user_states[user_id]['quest_requirements'] is not None:
            # This should be handled by the next step - processing the quest
            return
            
        # Store user's requirements description
        requirements = update.message.text
        
        # First try to detect language from Telegram's built-in language_code
        detected_language = 'ru'  # Default to Russian
        if user.language_code:
            lang_code = user.language_code.lower()
            if lang_code.startswith('en'):
                detected_language = 'en'
        
        # If we couldn't determine language from Telegram, fall back to text detection
        if detected_language == 'ru':
            fallback_detected_language = detect_language(requirements)
            if fallback_detected_language in ['en', 'ru']:
                detected_language = fallback_detected_language
        
        self.user_states[user_id]['user_language'] = detected_language
        
        try:
            logger.info(f"Generating quest for user {user_id} with requirements: {requirements}")
            
            from quest_engine import QuestEngine
            quest_engine = QuestEngine()
            
            # Create a temporary quest object to store in state
            quest_data = await quest_engine.generate_quest(requirements)
            
            if not quest_data:
                error_msg = "Извини, не удалось создать квест. Попробуй ещё раз с другими словами."
                await update.message.reply_text(error_msg)
                return
                
            # Store the generated quest in user state
            self.user_states[user_id]['quest_requirements'] = requirements
            self.user_states[user_id]['current_quest'] = quest_data
            
            # Start the quest from beginning
            start_step = quest_data['quest']['startStepId']
            self.user_states[user_id]['current_step_id'] = start_step
            self.user_states[user_id]['step_history'] = [start_step]
            self.user_states[user_id]['quest_started'] = True
            
            # Display first step
            await self.display_current_step(update, context)
            
        except Exception as e:
            logger.error(f"Error generating quest for user {user_id}: {str(e)}")
            if self.user_states[user_id]['user_language'] == 'en':
                error_msg = "An error occurred while creating the quest. Please try again."
            else:
                error_msg = "Произошла ошибка при создании квеста. Попробуй ещё раз."
            await update.message.reply_text(error_msg)
            
    async def display_current_step(self, update, context):
        """Display the current step of the quest."""
        user_id = update.effective_user.id
        if user_id not in self.user_states:
            return
            
        state = self.user_states[user_id]
        if not state['quest_started'] or not state['current_quest']:
            return
            
        # Get current step data
        quest_data = state['current_quest']
        steps_dict = {step['id']: step for step in quest_data['quest']['steps']}
        current_step = steps_dict.get(state['current_step_id'])
        
        if not current_step:
            await update.message.reply_text("Ошибка: не удалось найти текущий шаг квеста.")
            return
            
        # Format the message with options
        text = current_step['text']
        
        # Add emoji options for each choice
        if 'options' in current_step and len(current_step['options']) > 0:
            options_text = "\n"
            for i, option in enumerate(current_step['options'], 1):
                options_text += f"{option['emoji']} {option['text']}\n"
            
            # Use appropriate language for the prompt
            if state.get('user_language') == 'en':
                text += f"\n\nChoose an action:\n{options_text}"
            else:
                text += f"\n\nВыбери действие:\n{options_text}"
        
        await update.message.reply_text(text)
        
    async def handle_choice(self, update, context):
        """Handle user's choice and proceed to next step."""
        user_id = update.effective_user.id
        user = update.effective_user
        
        if user_id not in self.user_states:
            await self.new_quest(update, context)
            return
            
        if not self.user_states[user_id]['quest_started']:
            # If quest hasn't started yet, treat as requirements
            await self.handle_requirements(update, context)
            return
            
        user_choice = update.message.text
        
        try:
            state = self.user_states[user_id]
            quest_data = state['current_quest']
            
            if not quest_data:
                await update.message.reply_text("Ошибка: квест не загружен.")
                return
                
            # Get current step data
            steps_dict = {step['id']: step for step in quest_data['quest']['steps']}
            current_step = steps_dict.get(state['current_step_id'])
            
            if not current_step:
                await update.message.reply_text("Ошибка: текущий шаг не найден.")
                return
                
            # Detect language from Telegram's built-in language_code first
            detected_language = 'ru'  # Default to Russian
            if user.language_code:
                lang_code = user.language_code.lower()
                if lang_code.startswith('en'):
                    detected_language = 'en'
            
            # If we couldn't determine language from Telegram, fall back to text detection
            if detected_language == 'ru':
                fallback_detected_language = detect_language(user_choice)
                if fallback_detected_language in ['en', 'ru']:
                    detected_language = fallback_detected_language
            
            state['user_language'] = detected_language
            
            # Process the choice using QuestEngine
            from quest_engine import QuestEngine
            quest_engine = QuestEngine()
            
            next_step_id = await quest_engine.process_choice(current_step, user_choice, quest_data['quest']['steps'])
            
            if next_step_id:
                # Valid option found - proceed to next step
                state['current_step_id'] = next_step_id
                state['step_history'].append(next_step_id)
                
                # Display the new step
                await self.display_current_step(update, context)
            else:
                # No matching option - create a new branch
                logger.info(f"No matching option for user {user_id}, creating new branch...")
                new_step = await quest_engine.create_new_branch(current_step, user_choice, quest_data['quest']['steps'])
                
                if new_step:
                    # Add the new step to the quest data and proceed
                    quest_data['quest']['steps'].append(new_step)
                    state['current_step_id'] = new_step['id']
                    state['step_history'].append(new_step['id'])
                    
                    await self.display_current_step(update, context)
                else:
                    # If we can't create a new branch, just show an error
                    if detected_language == 'en':
                        await update.message.reply_text("Sorry, I didn't understand your choice. Try again!")
                    else:
                        await update.message.reply_text("Извини, я не понял твой выбор. Попробуй ещё раз!")
            
        except Exception as e:
            logger.error(f"Error processing choice for user {user_id}: {str(e)}")
            if state.get('user_language') == 'en':
                error_msg = "An error occurred while processing your choice. Please try again."
            else:
                error_msg = "Произошла ошибка при обработке твоего выбора. Попробуй ещё раз."
            await update.message.reply_text(error_msg)

    async def go_back(self, update, context):
        """Go back to the previous step."""
        user_id = update.effective_user.id
        
        if user_id not in self.user_states:
            return
            
        state = self.user_states[user_id]
        
        # Check if we have a history
        if len(state['step_history']) > 1:
            # Remove current step from history and go back to previous one
            state['step_history'].pop()  # Remove current step
            prev_step_id = state['step_history'][-1]  # Get the previous step
            state['current_step_id'] = prev_step_id
            
            await self.display_current_step(update, context)
        else:
            if state.get('user_language') == 'en':
                await update.message.reply_text("You're already at the first step of the quest!")
            else:
                await update.message.reply_text("Ты уже на первом шаге квеста!")

    def run(self):
        """Run the bot."""
        logger.info("KidQuestBot started.")
        # This would normally start the Telegram bot in a real implementation

# Create a global instance of the bot
bot = KidQuestBot()