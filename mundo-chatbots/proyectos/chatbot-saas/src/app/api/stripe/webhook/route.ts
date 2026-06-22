import Stripe from "stripe";
import { createClient } from "@supabase/supabase-js";
import { NextRequest } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!);

export async function POST(req: NextRequest) {
  const body = await req.text();
  const sig = req.headers.get("stripe-signature")!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return new Response("Webhook error", { status: 400 });
  }

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.CheckoutSession;
      // Activar suscripción del cliente
      await supabase.from("businesses").update({
        subscription_status: "active",
        stripe_customer_id: session.customer,
        plan: session.metadata?.plan || "starter",
      }).eq("email", session.customer_email);
      break;
    }

    case "customer.subscription.deleted": {
      const sub = event.data.object as Stripe.Subscription;
      // Desactivar cuando cancela
      await supabase.from("businesses").update({
        subscription_status: "cancelled",
      }).eq("stripe_customer_id", sub.customer);
      break;
    }

    case "invoice.payment_failed": {
      // Notificar al cliente que falló el pago
      const invoice = event.data.object as Stripe.Invoice;
      console.log("Pago fallido para:", invoice.customer_email);
      break;
    }
  }

  return new Response("OK", { status: 200 });
}
