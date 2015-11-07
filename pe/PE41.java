package me.starvii.pe;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class PE41 {
	static private boolean running = true;
	static private int n = 987654321;

	static final private Map<Integer, Set<Integer>> t = new HashMap<>();
	static {
		for(int i = 1; i <= 9; i++) {
			Set<Integer> s = new HashSet<>();
			for(int j = 1; j <= i; j++) {
				s.add(j);
			}
			t.put(i, s);
		}
	}
	
	static public boolean isPandigital(int n) {
		String sn = String.valueOf(n);
		int l = sn.length();
		if(l < 1 || l > 9) return false;
		Set<Integer> s0 = t.get(l);
		Set<Integer> s1 = new HashSet<>();
		for(int i = 0; i < sn.length(); i++) {
			char c = sn.charAt(i);
			if(c == '0') return false;
			int ic = c - '0';
			s1.add(ic);
		}
		return s0.equals(s1);
	}
	
	static public boolean isPrime(int n) {
		if(n < 2) return false;
		if(n == 2) return true;
		if(n % 2 == 0) return false;
		int q = 3;
		while(q * q <= n) {
			if(n % q == 0) return false;
			q += 2;
		}
		return true;
	}
	
	static public boolean filterN(int n) {
		final String t = "1379";
		String sn = String.valueOf(n);
		char c = sn.charAt(sn.length() - 1);
		int i = 0;
		for(i = 0; i < t.length(); i++) {
			if(c == t.charAt(i)) return true;
		}
		return false;
	}
	
	public static boolean isRunning() {
		return running;
	}

	public static void setRunning(boolean running) {
		PE41.running = running;
	}

	static public int getNextN() {
		synchronized(PE41.class){
			n = n % 2 == 0 ? n - 1 : n - 2;
			if(n < 10) return -1;
			return n;
		}
	}
	
	static public void main(String[] args) {
		for(int i = 0; i < 4; i++) {
			PanPrime r = new PanPrime();
			r.setThread(i);
			new Thread(r).start();
		}
	}
}

class PanPrime implements Runnable {
	private int thread;
	
	public int getThread() {
		return thread;
	}

	public void setThread(int thread) {
		this.thread = thread;
	}
	
	@Override
	public void run() {
		while(PE41.isRunning()) {
			int n = PE41.getNextN();
			if(n == -1) {
				PE41.setRunning(false);
				System.out.println("find no prime pandigital.");
			}
			if(PE41.filterN(n)) {
				if(PE41.isPandigital(n)) {
					System.out.println(thread + ": " + n);
					if(PE41.isPrime(n)) {
						PE41.setRunning(false);
						System.out.println("prime pandigital is " + n);
					}
				}
			}
		}
	}
}
