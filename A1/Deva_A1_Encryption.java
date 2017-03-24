import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Deva_A1_Encryption {

    private static List<Integer> generateKey(String cFilePath, String zFilePath, int keyLength) {

        List<Integer> z = new ArrayList<>();
        List<Integer> c = new ArrayList<>();


        try {

            FileReader cFile = new FileReader(cFilePath);
            BufferedReader cBr = new BufferedReader(cFile);
            String cLine;
            while ((cLine = cBr.readLine()) != null) {
                for (int i = 0; i < cLine.length(); i++) {
                    char cChar = cLine.charAt(i);
                    int cInt = Character.getNumericValue(cChar);
                    c.add(i, cInt);
                }
            }
            cBr.close();

            FileReader zFile = new FileReader(zFilePath);
            BufferedReader zBr = new BufferedReader(zFile);
            String zLine;
            while ((zLine = zBr.readLine()) != null) {
                for (int i = 0; i < zLine.length(); i++) {
                    char zChar = zLine.charAt(i);
                    int zInt = Character.getNumericValue(zChar);
                    z.add(i, zInt);
                }
            }
            zBr.close();

            for (int i = 0; i < keyLength - 32; i++) {
                int term = 0;
                for (int j = 0; j < 32; j++) {
                    int product = c.get(j) * z.get(i + j);
                    term = term + product;
                }
                term = term % 2;
                z.add(term);
            }


        } catch (IOException e) {
            e.printStackTrace();
        }
        return z;

    }

    private static void encryptMessage(String messageFilePath, String cFilePath, String zFilePath) {

        List<Integer> encryptedMessage = new ArrayList<>();

        try {
            List<Integer> message = new ArrayList<>();
            FileReader messageFile = new FileReader(messageFilePath);
            BufferedReader messageBr = new BufferedReader(messageFile);
            String messageLine;

            while ((messageLine = messageBr.readLine()) != null) {

                for (int i = 0; i < messageLine.length(); i++) {
                    char messageChar = messageLine.charAt(i);
                    int messageInt = Character.getNumericValue(messageChar);
                    message.add(i, messageInt);
                }

                System.out.println("Message from file: ");

                for(Integer msg : message){
                    System.out.print(msg);
                }

                System.out.println();

                List<Integer> zKey = generateKey(cFilePath, zFilePath, messageLine.length());

                System.out.println("Key is : ");

                for(Integer bit : zKey){
                    System.out.print(bit);
                }

                System.out.println();

                Integer sum;
                for (int i = 0; i < message.size(); i++) {
                    sum = zKey.get(i) + message.get(i);
                    sum = sum % 2;
                    encryptedMessage.add(sum);
                }


                System.out.println("Message is encrypted! Encrypted Message is : ");

                for(Integer encryptedMsg : encryptedMessage){
                    System.out.print(encryptedMsg);
                }

                System.out.println();


            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public static void main(String[] args) {

        String messageFilePath = "x.txt";
        String cFilePath = "c.txt";
        String zFilePath = "z.txt";
        encryptMessage(messageFilePath, cFilePath, zFilePath);



    }

}