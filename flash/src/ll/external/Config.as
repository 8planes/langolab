package ll.external {
    import mx.core.FlexGlobals;
    
    public class Config {
        private static function stringProperty(name : String) : String {
            var value : * = FlexGlobals.topLevelApplication.parameters[name];
            return value ? String(value) : null;
        }
        public static function get cirrusUrl() : String {
            return stringProperty('cirrus_url');
        }
        public static function get stompLogin() : String {
            return stringProperty('stomp_login');
        }
        public static function get stompPassword() : String {
            return stringProperty('stomp_password');
        }
        public static function get stompServer() : String {
            return stringProperty('stomp_server');
        }
        public static function get stompPort() : int {
            return parseInt(stringProperty("stomp_port"));
        }
        public static function get stompSubscribeDestination() : String {
            return stringProperty("stomp_subscribe_destination");
        }
    }
}