"""
Payment Event Publisher
Publish các event thanh toán cho WebSocket clients
"""
import json
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


class PaymentEventPublisher:
    """
    Publisher cho các event thanh toán
    Gửi events qua Django Channels để WebSocket clients nhận được real-time updates
    """

    def __init__(self):
        self.channel_layer = get_channel_layer()

    def publish(self, event_type: str, data: dict):
        """
        Publish payment event
        
        Args:
            event_type: Loại event (PAYMENT_SUCCESS, PAYMENT_FAILED, etc.)
            data: Dữ liệu event
        """
        if not self.channel_layer:
            logger.warning("⚠️ Channel layer not configured. Event not published.")
            return

        try:
            event_name = settings.PAYMENT_EVENTS.get(event_type, event_type)

            logger.info(f"📢 Publishing event: {event_name}")
            logger.info(f"📦 Event data: {data}")

            # Gửi đến group channel theo order_id
            order_id = data.get('order_id')
            if order_id:
                async_to_sync(self.channel_layer.group_send)(
                    f"payment_{order_id}",
                    {
                        'type': 'payment_event',
                        'event': event_name,
                        'data': data
                    }
                )

            # Gửi đến broadcast channel (tất cả listeners)
            async_to_sync(self.channel_layer.group_send)(
                "payment_broadcast",
                {
                    'type': 'payment_event',
                    'event': event_name,
                    'data': data
                }
            )

            logger.info(f"✅ Event {event_name} published successfully")

        except Exception as e:
            logger.error(f"❌ Error publishing event: {str(e)}")

    def payment_created(self, order_id: str, payment_id: str, amount: float, order_code: int, payment_url: str = None, qr_code: str = None):
        """Event: Tạo payment mới"""
        self.publish('PAYMENT_PENDING', {
            'order_id': str(order_id),
            'payment_id': str(payment_id),
            'amount': float(amount),
            'order_code': order_code,
            'payment_url': payment_url,
            'qr_code': qr_code,
            'timestamp': self._get_timestamp()
        })

    def payment_success(self, order_id: str, payment_id: str, amount: float, transaction_id: str = None):
        """Event: Thanh toán thành công"""
        self.publish('PAYMENT_SUCCESS', {
            'order_id': str(order_id),
            'payment_id': str(payment_id),
            'amount': float(amount),
            'transaction_id': transaction_id or '',
            'timestamp': self._get_timestamp()
        })

    def payment_failed(self, order_id: str, payment_id: str, reason: str):
        """Event: Thanh toán thất bại"""
        self.publish('PAYMENT_FAILED', {
            'order_id': str(order_id),
            'payment_id': str(payment_id),
            'reason': reason,
            'timestamp': self._get_timestamp()
        })

    def payment_cancelled(self, order_id: str, payment_id: str):
        """Event: Hủy thanh toán"""
        self.publish('PAYMENT_CANCELLED', {
            'order_id': str(order_id),
            'payment_id': str(payment_id),
            'timestamp': self._get_timestamp()
        })

    def _get_timestamp(self):
        """Lấy timestamp hiện tại"""
        return datetime.now().isoformat()


# Singleton instance
payment_publisher = PaymentEventPublisher()