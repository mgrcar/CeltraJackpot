
/**
 * Created with IntelliJ IDEA.
 * User: Matej Kočevar
 * Date: 19.9.2014
 * Time: 20:33
 */



public class gambler {
    

    public static void main(String args[]){
        long start = System.currentTimeMillis();
        String adress = args[0];
        double eps, E =50; //Epsilon

        int machines = web.getHTMLresponse(adress + "/machines");
        int pulls = web.getHTMLresponse(adress + "/pulls");
        System.out.println("You have "+machines+" machines and "+pulls+" pulls available.");

        int[][] machineStats = new int[machines][2];   //pulls: [profitable][all]
        for (int i=0;i<machineStats.length;i++){for (int j=0;j<machineStats[i].length;j++){machineStats[i][j]=0;}}
        machine.probability = new double[machines];

        int pullNo=1;
        int reward=0;
        int machineCurrent= math.random(machines)-1, machineLast=-1;
        int odg;

        while (true){
            if (pullNo==pulls+1)break;

            //pull
            System.out.print(pullNo+". ");
            odg=web.getHTMLresponse(adress+"/"+(machineCurrent+1)+"/"+pullNo);
            machineStats[machineCurrent][1]++;
            if (odg==1){
                reward++;
                machineStats[machineCurrent][0]++;
            }
            pullNo++;
            for (int i=0;i<machineStats.length;i++) {
                machine.probability[i] = (machineStats[i][1])==0? 0 : machineStats[i][0] / (double)(machineStats[i][1]);
                System.out.print(machineStats[i][0] + ":" + (machineStats[i][1]));
                System.out.printf("{%.2f} ",machine.probability[i]*100);
            }

            //set new Epsilon
            eps = (100-(pullNo/pulls)*100)*(E/100);

            //choose next machine
            machineCurrent=machine.choose(eps, machineStats, machineCurrent);
            if (machineLast != machineCurrent) {
                machineLast = machineCurrent;
                System.out.println(" ["+(machineCurrent+1)+"]");
            }
            else System.out.println();
        }

        //statistics
        double max = math.returnLargest(machine.probability);
        System.out.println("Gain: "+reward+"/"+pulls);
        System.out.printf("Regret: %.2f", (max - (reward / (double) pulls)) * 100);
        System.out.println("%");
        System.out.printf("Duration: %.2fs",((double)System.currentTimeMillis()-start)/1000);
        System.exit(reward);
    }
}