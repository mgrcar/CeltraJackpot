import java.util.Random;

/**
 * Created with IntelliJ IDEA.
 * User: Matej
 * Date: 7.11.2014
 * Time: 1:33
 */
public class math {
    static int random(int max){
        Random rand = new Random();
        return rand.nextInt(max) + 1;
    }
    static int random(int exclude, int max){
        Random rand = new Random();
        int r = exclude+1;
        while (r==exclude+1)
            r=rand.nextInt(max) + 1;
        return r;
    }

    static double returnLargest(double array[]){
        double max = array[0];
        for (double temp :array)
            if (temp > max)
                max = temp;
        return max;
    }
}
