/**
 * Created with IntelliJ IDEA.
 * User: Matej
 * Date: 7.11.2014
 * Time: 1:41
 */
public class machine {
    static double[]probability;

    static int choose(double eps, int[][]stats, int machineCurrent){
        if (math.random(100)<=eps){
            //exploration
            int r = math.random(machineCurrent, stats.length)-1;
            System.out.print(" !"+(r+1)+"! ");
            return r;
        }

        else {
            //exploitation
            int index=0;
            double max = probability[index];
            int min=0;
            for (int i=0; i<probability.length; i++) {
                if (probability[i] > max) {
                    max = probability[i];
                    index=i;
                }
                else if (probability[i] == max){
                    for (int j=0; j<stats.length; j++){
                        if (stats[j][1]<min) {
                            min = stats[j][i];
                            index = j;
                        }
                    }
                }
            }
            return index;
        }
    }
}
