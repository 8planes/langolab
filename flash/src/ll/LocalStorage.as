package ll {
    import flash.net.SharedObject;
    
    public class LocalStorage {
        private static function get localSO() : SharedObject {
            return SharedObject.getLocal("ll", "/");
        }
        public static function get cleared() : Boolean {
            if (localSO.data.hasOwnProperty("cleared"))
                return localSO.data.cleared;
            else
                return false;                    
        }
        public static function set cleared(value : Boolean) : void {
            localSO.data.cleared = value;
            localSO.flush();
        }
    }
}