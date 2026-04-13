from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self):
        """Initialize the Hugging Face sentiment analysis pipeline."""
        try:
            # Load a lightweight sentiment analysis model
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            logger.info("Inference engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize inference engine: {str(e)}")
            raise

    def analyze_ticket(self, ticket_text: str) -> dict:
        """
        Analyze customer ticket text for intent and sentiment.

        Args:
            ticket_text (str): The customer ticket text to analyze

        Returns:
            dict: Analysis results containing intent, confidence, and sentiment
        """
        try:
            # Perform sentiment analysis
            sentiment_results = self.sentiment_pipeline(ticket_text)

            # Extract the highest confidence sentiment
            if sentiment_results and len(sentiment_results) > 0:
                # sentiment_results is a list of lists (one per input)
                scores = sentiment_results[0]

                # Find the sentiment with highest score
                best_sentiment = max(scores, key=lambda x: x['score'])
                sentiment = best_sentiment['label'].lower()
                confidence = best_sentiment['score']
            else:
                sentiment = "neutral"
                confidence = 0.0

            # Determine intent based on sentiment and keywords
            intent = self._classify_intent(ticket_text, sentiment)

            result = {
                "intent": intent,
                "confidence": confidence,
                "sentiment": sentiment,
                "raw_sentiment_scores": scores if 'scores' in locals() else []
            }

            logger.info(f"Ticket analysis complete: intent={intent}, sentiment={sentiment}, confidence={confidence:.3f}")
            return result

        except Exception as e:
            logger.error(f"Error analyzing ticket: {str(e)}")
            return {
                "intent": "error",
                "confidence": 0.0,
                "sentiment": "neutral",
                "error": str(e)
            }

    def _classify_intent(self, text: str, sentiment: str) -> str:
        """
        Classify the intent based on text content and sentiment.

        This is a simple rule-based classifier. In production, you might use
        a more sophisticated intent classification model.
        """
        text_lower = text.lower()

        # Complaint keywords
        complaint_keywords = [
            "problem", "issue", "broken", "not working", "error", "fail",
            "disappointed", "unhappy", "complaint", "refund", "cancel"
        ]

        # Inquiry keywords
        inquiry_keywords = [
            "how", "what", "when", "where", "why", "help", "support",
            "question", "information", "details", "status"
        ]

        # Praise keywords
        praise_keywords = [
            "great", "excellent", "amazing", "love", "perfect", "thank you",
            "awesome", "fantastic", "wonderful"
        ]

        # Feature request keywords
        feature_keywords = [
            "suggest", "would like", "add", "feature", "improve", "enhance",
            "new", "request", "wish"
        ]

        # Check for complaint intent
        if any(keyword in text_lower for keyword in complaint_keywords) or sentiment in ["negative", "label_0"]:
            return "complaint"

        # Check for inquiry intent
        if any(keyword in text_lower for keyword in inquiry_keywords):
            return "inquiry"

        # Check for praise intent
        if any(keyword in text_lower for keyword in praise_keywords) or sentiment in ["positive", "label_2"]:
            return "praise"

        # Check for feature request
        if any(keyword in text_lower for keyword in feature_keywords):
            return "feature_request"

        # Default to general feedback
        return "general_feedback"