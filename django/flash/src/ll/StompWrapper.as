package ll {
    import flash.events.EventDispatcher;
    
    import ll.external.Config;
    import ll.external.OutgoingCalls;
    
    import org.codehaus.stomp.Stomp;
    import org.codehaus.stomp.event.ConnectedEvent;
    import org.codehaus.stomp.event.MessageEvent;
    import org.codehaus.stomp.event.STOMPErrorEvent;
    import org.codehaus.stomp.headers.ConnectHeaders;
    
    [Event(name="connected", type="org.codehaus.stomp.event.ConnectedEvent")]
    public class StompWrapper extends EventDispatcher {
        private static var _instance : StompWrapper;
        
        public static function get instance() : StompWrapper {
            if (_instance == null)
                _instance = new StompWrapper();
            return _instance;
        }
        
        private var _stomp : Stomp;
        private var _connected : Boolean = false;
        private var _currentMatchChannel : String = null;
        private var _toExecuteOnConnect : Array = [];

        public function StompWrapper() {
            var ch : ConnectHeaders = new ConnectHeaders();
            ch.login = Config.stompLogin;
            ch.passcode = Config.stompPassword;
            _stomp = new Stomp();
            _stomp.addEventListener(
                ConnectedEvent.CONNECTED,
                connectHandler);
            _stomp.addEventListener(STOMPErrorEvent.ERROR,
                function(event : STOMPErrorEvent) : void {
                    Logger.log("STOMPErrorEvent: " + 
                        event.error.body.toString());
                });
            _stomp.addEventListener(
                MessageEvent.MESSAGE,
                messageHandler);
            _stomp.connect(Config.stompServer, Config.stompPort, ch);
            Logger.log('Connecting stomp to ' + 
                Config.stompSubscribeDestination);
            _stomp.subscribe(Config.stompSubscribeDestination);
        }
        public function get connected() : Boolean {
            return _connected;
        }
        public function connectToMatch(matchID : int) : void {
            var newMatchChannel : String = "/llmatch/" + matchID;
            if (connected)
                connectToMatchImpl(newMatchChannel);
            else
                _toExecuteOnConnect.push(function() : void {
                    connectToMatchImpl(newMatchChannel);
                });
        }
        
        private function messageHandler(event : MessageEvent) : void {
            var destination : String = event.message.headers['destination'];
            var message : String = event.message.body.toString();
            if (destination == Config.stompSubscribeDestination)
                OutgoingCalls.messageReceived(message);
            else if (destination == _currentMatchChannel)
                OutgoingCalls.matchMessageReceived(message);
        }
        
        private function connectHandler(event : ConnectedEvent) : void {
            _connected = true;
            Logger.log("Stomp is connected");
            dispatchEvent(new ConnectedEvent(ConnectedEvent.CONNECTED));
            for each (var fn : Function in _toExecuteOnConnect)
            fn();
            _toExecuteOnConnect = [];
        }
        
        private function connectToMatchImpl(newMatchChannel : String) : void {
            if (_currentMatchChannel != null)
                _stomp.unsubscribe(_currentMatchChannel);
            Logger.log('Connecting stomp to ' +
                newMatchChannel);
            _stomp.subscribe(newMatchChannel);
            _currentMatchChannel = newMatchChannel;
        }
    }
}