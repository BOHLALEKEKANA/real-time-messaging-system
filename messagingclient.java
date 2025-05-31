import java.net.URI;
import javax.websocket.*;
import java.io.IOException;

@ClientEndpoint
public class MessagingClient {
    private Session session;
    private String userId;

    public MessagingClient(String userId, String serverUri) {
        this.userId = userId;
        try {
            WebSocketContainer container = ContainerProvider.getWebSocketContainer();
            container.connectToServer(this, new URI(serverUri + "/ws/" + userId));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @OnOpen
    public void onOpen(Session session) {
        this.session = session;
        System.out.println(userId + " connected to server");
    }

    @OnMessage
    public void onMessage(String message) {
        System.out.println(userId + " received: " + message);
    }

    @OnClose
    public void onClose(Session session, CloseReason reason) {
        System.out.println(userId + " disconnected: " + reason);
    }

    public void sendMessage(String recipient, String content) {
        try {
            String message = String.format("{\"sender\":\"%s\",\"recipient\":\"%s\",\"content\":\"%s\"}",
                    userId, recipient, content);
            session.getBasicRemote().sendText(message);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        // Example usage
        MessagingClient userA = new MessagingClient("user_a", "ws://localhost:8000");
        MessagingClient userB = new MessagingClient("user_b", "ws://localhost:8000");

        // Simulate User A sending a message to User B
        userA.sendMessage("user_b", "Hello, how are you?");
        
        // Keep the client running
        try {
            Thread.sleep(5000); // Wait for messages
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}