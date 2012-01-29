package ll.external {
    import flash.events.Event;

    public class MatchEvent extends Event {
        public static const MATCH : String = "match";
        
        private var _matchID : String;
        
        public function MatchEvent(matchID : String) {
            super(MATCH, false, false);
            this._matchID = matchID;
        }
        public function get matchID() : String {
            return _matchID;
        }
    }
}