from context import (
    FI_STRIPE_API_KEY,
    FI_STRIPE_WEBHOOK_KEY,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)
import stripe
from typing import (
    Optional,
)

stripe.api_key = FI_STRIPE_API_KEY


async def main(request: Request) -> JSONResponse:
    """Parse webhook request and execute event"""
    body: Optional[bytes] = await request.body()
    signature: Optional[str] = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            body,
            signature,
            FI_STRIPE_WEBHOOK_KEY,
        )
    except ValueError:
        print("Invalid payload")
        return JSONResponse(
            {
                "message": "Invalid payload",
                "error": True,
            }
        )
    except stripe.error.SignatureVerificationError:
        return JSONResponse(
            {
                "message": "Invalid signature",
                "error": True,
            }
        )

    if event.type == "payment_intent.succeeded":
        print("PaymentIntent was successful!")
    else:
        print(f"Unhandled event type {event.type}")

    return JSONResponse(
        {
            "message": "OK",
            "error": False,
        }
    )
