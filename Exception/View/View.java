package View;

import java.util.Scanner;

import Presenter.Presenter;

public class View {

    private Presenter presenter;
    private Scanner sc;

    public View(){
        this.presenter = new Presenter();
        this.sc = new Scanner(System.in);
    }

    public void exit() {
        System.out.println("Good bye");
        System.exit(0);
    } 

    public void start(){        
        System.out.println("Для выхода из приложения нажмите последовательно 'q' и 'Enter' ");
        System.out.println("Введите данные в произвольном порядке, разделенные пробелом: Фамилия Имя Отчество датарождения номертелефона пол.");
        String s;
        while (true){
            s = sc.nextLine();
            if (s.equalsIgnoreCase("q")){
                exit();
            }
            this.presenter.setInputString(s);
            System.out.println(this.presenter.getString());
        }
       
        
        
    }

}
