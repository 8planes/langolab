package ll {
    import ll.external.OutgoingCalls;

    public class Logger {
        public static function log(message : String) : void {
            OutgoingCalls.log(message);
        }
    }
}