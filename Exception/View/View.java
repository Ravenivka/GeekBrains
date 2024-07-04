package View;

import java.util.Scanner;

import Presenter.Presenter;

public class View {

    private Presenter presenter;

    public View(){
        this.presenter = new Presenter(this);
    }

    public void start(){
        Scanner sc = new Scanner(System.in);
        System.out.println("Введите данные в произвольном порядке, разделенные пробелом: Фамилия Имя Отчество датарождения номертелефона пол.");
        String s = sc.nextLine();
        sc.close();
        this.presenter.setInputString(s);
        this.presenter.translate();
        System.out.println(this.presenter.getOutString());
    }

}
