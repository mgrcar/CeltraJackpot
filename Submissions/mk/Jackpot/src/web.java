import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;

/**
 * Created with IntelliJ IDEA.
 * User: Matej
 * Date: 7.11.2014
 * Time: 1:37
 */
public class web {
    static int getHTMLresponse (String path) {
        try {
            URL url = new URL(path);
            BufferedReader in = new BufferedReader( new InputStreamReader(url.openStream()));
            String value = in.readLine();
            try {
                return Integer.parseInt(value);
            } catch (Exception e){
                System.out.println("Unexpected respond from server: "+value);
                return -1;
            }
        } catch (Exception e){
            System.out.println("Error: "+e);
            System.out.close();
            return -1;
        }
    }
}
