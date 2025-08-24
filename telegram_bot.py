import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class KidQuestBot:
    def __init__(self):
        # For now we'll create a mock implementation that doesn't require external dependencies
        self.user_states: Dict[int, Dict[str, Any]] = {}
        
    async def start(self, update, context):
        """Send welcome message when /start command is issued."""
        welcome_text = (
            "👋 Привет! Я KidQuestBot - твой помощник в создании "
            "восхитительных текстовых квестов для детей!\n\n"
            "Напиши /new, чтобы начать новый квест!"
        )
        await update.message.reply_text(welcome_text)
        
    async def new_quest(self, update, context):
        """Initiate a new quest by asking for requirements."""
        user_id = update.effective_user.id
        
        # Clear any existing state for this user
        if user_id in self.user_states:
            del self.user_states[user_id]
            
        # Set initial state
        self.user_states[user_id] = {
            'quest_requirements': None,
            'current_quest': None,
            'current_step_id': None,
            'step_history': [],
            'quest_started': False
        }
        
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
        
        try:
            logger.info(f"Generating quest for user {user_id} with requirements: {requirements}")
            
            # For demo purposes, we'll use a mock implementation that doesn't require external dependencies
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
            
            # Display first step (mock implementation)
            await self.display_current_step(update, context)
            
        except Exception as e:
            logger.error(f"Error generating quest for user {user_id}: {str(e)}")
            error_msg = "Произошла ошибка при создании квеста. Попробуй ещё раз."
            await update.message.reply_text(error_msg)
            
    async def display_current_step(self, update, context):
        """Display the current step of the quest (mock implementation)."""
        user_id = update.effective_user.id
        if user_id not in self.user_states:
            return
            
        # For demo purposes, we'll just show a simple message
        await update.message.reply_text(
            "Это демонстрационная версия. В реальной реализации здесь будет отображаться "
            "текст сценария и варианты выбора."
        )
        
    async def handle_choice(self, update, context):
        """Handle user's choice and proceed to next step (mock implementation)."""
        user_id = update.effective_user.id
        
        if user_id not in self.user_states:
            await self.new_quest(update, context)
            return
            
        if not self.user_states[user_id]['quest_started']:
            # If quest hasn't started yet, treat as requirements
            await self.handle_requirements(update, context)
            return
            
        user_choice = update.message.text
        
        try:
            # For demo purposes, we'll just show a response
            await update.message.reply_text(
                f"Ты выбрал: '{user_choice}'. В реальной реализации это будет обработано "
                "с использованием LLM для определения подходящего варианта."
            )
            
        except Exception as e:
            logger.error(f"Error processing choice for user {user_id}: {str(e)}")
            error_msg = "Произошла ошибка при обработке твоего выбора. Попробуй ещё раз."
            await update.message.reply_text(error_msg)

    async def go_back(self, update, context):
        """Go back to the previous step (mock implementation)."""
        user_id = update.effective_user.id
        
        if user_id not in self.user_states:
            return
            
        # For demo purposes
        await update.message.reply_text("Возврат к предыдущему шагу (в реальной реализации)")

    def run(self):
        """Run the bot - mock implementation."""
        logger.info("KidQuestBot started. In a real implementation, this would start the Telegram bot.")
        # This is just a placeholder for now

# Create a global instance of the bot
bot = KidQuestBot()