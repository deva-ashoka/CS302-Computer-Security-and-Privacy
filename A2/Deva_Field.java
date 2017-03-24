import java.util.Scanner;

public class Deva_Field {

    public static int[] binaryExpression = new int[128];


    public static String getMultiplicativeInverse(String input) {

        int i = 0;
        while (Integer.parseInt(input) != binaryExpression[i]) {
            i++;
        }
        return Integer.toString(binaryExpression[127 - i]);
    }


    public static String getAdditiveInverse(String input) {
        return input;
    }


    public static String[] makeStringsEqualLength(String input1, String input2) {
        String[] input = new String[2];
        int length1 = input1.length();
        int length2 = input2.length();
        if (length1 < length2) {
            for (int i = 0; i < length2 - length1; i++) {
                input1 = '0' + input1;
            }
            input[0] = input1;
            input[1] = input2;
            return input;

        } else if (length2 < length1) {
            for (int i = 0; i < length1 - length2; i++) {
                input2 = '0' + input2;
            }
        }
        input[0] = input1;
        input[1] = input2;
        return input;
    }


    public static String addBinaryInputs(String input1, String input2) {

        String result = "";

        String[] input = makeStringsEqualLength(input1, input2);
        input1 = input[0];
        input2 = input[1];

        String[] array1 = input1.split("");
        String[] array2 = input2.split("");

        int carry = 0;

        for (int i = array1.length - 1; i >= 0; i--) {

            int bit1 = Integer.parseInt(array1[i]);
            int bit2 = Integer.parseInt(array2[i]);

            int sum = (bit1 ^ bit2 ^ carry);

            result = sum + result;
        }
        return result;


    }


    public static void main(String[] args) {

        try {

            //generator chosen = x

            for (int i = 0; i < 7; i++) {
                int temp = (int) Math.pow(2, i);
                String binaryOfTemp = Integer.toBinaryString(temp);
                temp = Integer.parseInt(binaryOfTemp);
                binaryExpression[i] = temp;
            }

            // f(x) = X^7 + x + 1 = 0
            // => x^7 = (-x - 1) (mod 2)
            // => x^7 = x + 1
            binaryExpression[7] = 11;

            for (int i = 8; i < 128; i++) {
                binaryExpression[i] = binaryExpression[i - 1] * 10;
                String temp = Integer.toString(binaryExpression[i]);
                if (temp.length() > 7) {
                    temp = temp.substring(1, temp.length());
                    temp = addBinaryInputs(temp, "11");
                    binaryExpression[i] = Integer.parseInt(temp);
                }
            }

            for (int i = 0; i < binaryExpression.length; i++) {
                System.out.println("X^" + i + " : " + binaryExpression[i]);
            }

            while (true) {

                Scanner sc = new Scanner(System.in);
                System.out.println("Enter the input for which you want Additive Inverse or Multiplicative Inverse:");
                String input = sc.nextLine();

                //checking if the input is valid
                boolean doesInputExist = false;
                for (int i = 0; i < 128; i++) {
                    if (Integer.parseInt(input) == binaryExpression[i]) {
                        doesInputExist = true;
                    }
                }

                if (doesInputExist) {

                    System.out.println("Enter 'a' for Additive Inverse or 'm' for Multiplicative Inverse");
                    String operation = sc.nextLine();

                    if (operation.equals("a")) {
                        String additiveInverse = getAdditiveInverse(input);
                        System.out.println("Additive Inverse: " + additiveInverse);
                    }

                    if (operation.equals("m")) {
                        String multiplicativeInverse = getMultiplicativeInverse(input);
                        System.out.println("Multiplicative Inverse: " + multiplicativeInverse);
                    }
                } else {
                    System.out.println("Invalid Input!");
                }
            }


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}

