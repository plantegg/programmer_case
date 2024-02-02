import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class SpinLockAccumulator {
    private AtomicInteger sum = new AtomicInteger(0);
    private AtomicBoolean lock = new AtomicBoolean(false);

	// Declare the native method
    private static native void pauseInstruction();

    // Load the native library containing the implementation of pauseInstruction
    static {
        System.loadLibrary("pause");
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("请提供两个参数：线程数量和循环次数");
            return;
        }

        int numThreads = Integer.parseInt(args[0]);
        int totalIncrements = Integer.parseInt(args[1]);

        SpinLockAccumulator accumulator = new SpinLockAccumulator();

        Thread[] threads = new Thread[numThreads];
        long startTime = System.currentTimeMillis(); // 记录开始时间

        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                int incrementsPerThread = totalIncrements / numThreads + 
                                         (totalIncrements % numThreads == 0 ? 0 : 1);
                for (int j = 0; j < incrementsPerThread; j++) {
                    try{
					    accumulator.add(); }
					catch(Exception e){}
				
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

		long endTime = System.currentTimeMillis(); // 记录结束时间
        long totalTime = endTime - startTime; // 计算总耗时

        System.out.println("累加结果: " + accumulator.getSum());
        System.out.println("操作耗时: " + totalTime + " 毫秒");
    }

    public void add() throws Exception {
        while (true) {
            if (lock.compareAndSet(false, true)) {
                try {
                    sum.incrementAndGet();
                } finally {
                    lock.set(false);
                }
                break;
            }
            // 在实际项目中，可能需要在此处添加Thread.yield()或者Thread.sleep(1)
            // 以避免过度消耗CPU资源。
			//pauseInstruction();
			Thread.sleep(1);
        }
    }

    public int getSum() {
        return sum.get();
    }
}

