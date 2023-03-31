

import java.lang.*;
import java.util.ArrayList;
import java.lang.management.*;

public class HighUS {
	public static void main(String[] args) throws Exception{
		HighUS us = new HighUS();
		us.run();
	}
	
	private void run() throws Exception{
		int count = java.lang.Runtime.getRuntime().availableProcessors();
		
		for(int i=0; i<count/2; ++i){
			new Thread(new ConsumeCPUTask()).start();
		}
		
		for(int i=0; i<10; ++i){
			new Thread(new NotConsumeCPUTask()).start();
		}
	}
	
	class ConsumeCPUTask implements Runnable{
		public void run(){
			String str="kkkfdkfdkkfekkewrenf n few jfejewjew@#$%^43939u2jf"+"abkke45"+"98430985458744kjdfd";
			float i=0.002f;
			float j=232.123456f;
			
			while(true){
				j=i*j;
				str.indexOf("#");
				ArrayList<String> list = new ArrayList<String>();
				for(int k=0; k<10000; ++k){
					list.add(str+String.valueOf(k));
				}
				list.contains("AXXXA");
			}
		}
	}
	
	class NotConsumeCPUTask implements Runnable{
		
		public void run(){
			
			while(true){
				try{
					Thread.sleep(1000);
				}catch(InterruptedException e){
					e.printStackTrace();
				}
			}
		}
	}

}
