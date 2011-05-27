package ll.external {
    import flash.events.EventDispatcher;
    import flash.external.ExternalInterface;

    [Event(name="match", type="ll.external.MatchEvent")]
    [Event(name="match_ended", type="ll.external.MatchEndedEvent")]
    public class IncomingCalls extends EventDispatcher {
        private static var _instance : IncomingCalls = null;

        public function IncomingCalls() {
            var that : IncomingCalls = this;
            ExternalInterface.addCallback(
                "matchWith",
                function(matchID : String) : void {
                    that.dispatchEvent(new MatchEvent(matchID));
                });
            ExternalInterface.addCallback(
                "matchEnded",
                function() : void {
                    that.dispatchEvent(new MatchEndedEvent());
                });
        }

        public static function get instance() : IncomingCalls {
            if (_instance == null)
                _instance = new IncomingCalls();
            return _instance;
        }
    }
}