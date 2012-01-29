package ll.external {
    import flash.external.ExternalInterface;

    public class OutgoingCalls {
        /**
         * 0 means that we're trying to get through security.
         * 1 means that we made it through security and that we're 
         *     trying to connect to stomp server, etc.
         * When everything is ready to go, we call ready.
         */
        public static function stateChange(state : int) : void {
            ExternalInterface.call("swfout.stateChange", state);
        }
        public static function ready(nearID : String) : void {
            ExternalInterface.call("swfout.ready", nearID);
        }
        public static function messageReceived(message : String) : void {
            ExternalInterface.call("swfout.messageReceived", message);
        }
        public static function matchMessageReceived(message : String) : void {
            ExternalInterface.call("swfout.matchMessageReceived", message);
        }
        public static function log(message : String) : void {
            ExternalInterface.call("swfout.flashDebug", message);
        }
        public static function track(pageName : String) : void {
            ExternalInterface.call("swfout.track", pageName);
        }
    }
}