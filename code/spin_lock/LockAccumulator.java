public class LockAccumulator {
    private int sum = 0; // 变量用于累加
    private final Object lock = new Object(); // 自选的锁对象

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("请提供两个参数：线程数量和循环次数");
            return;
        }

        int numThreads = Integer.parseInt(args[0]);
        int totalIncrements = Integer.parseInt(args[1]);

        LockAccumulator accumulator = new LockAccumulator();

        Thread[] threads = new Thread[numThreads];
		long start = System.currentTimeMillis();

        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                int incrementsPerThread = totalIncrements / numThreads;
                for (int j = 0; j < incrementsPerThread; j++) {
                    accumulator.add();
                }
            });
            threads[i].start();
        }

        // 等待所有线程完成
        for (int i = 0; i < numThreads; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
		long end = System.currentTimeMillis();
        System.out.println("累加结果: " + accumulator.getSum()  + " and time:" +(end-start));
    }

    public void add() {
        synchronized (lock) {
            sum++;
        }
    }

    public int getSum() {
        synchronized (lock) {
            return sum;
        }
    }
}

