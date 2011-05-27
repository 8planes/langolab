package ll.external {
    import flash.events.Event;
    
    public class MatchEndedEvent extends Event {
        public static const MATCH_ENDED : String = "match_ended";
        
        public function MatchEndedEvent() {
            super(MATCH_ENDED, false, false);
        }
    }
}