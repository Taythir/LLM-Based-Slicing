package com.acctmgr;

import org.junit.Test;
import static org.junit.Assert.*;

public class TransferDeadlockTest {
    
    /**
     * Basic test that only exercises the SAFE path
     * Slicer4J slicing from this test will ONLY capture:
     * - transferWithLockOrdering method
     * - The safe lock ordering logic
     * 
     * It will MISS:
     * - transferDirectLocking method (deadlock-prone)
     * - bulkTransfer method (also deadlock-prone)
     * - The dangerous locking patterns
     */
    @Test
    public void testBasicTransfer() {
        Account account = new Account();
        
        // useOptimizedPath defaults to false, so only safe path executes
        Thread t1 = new Thread(() -> {
            account.transfer(1, 2, 100);
        });
        
        Thread t2 = new Thread(() -> {
            account.transfer(2, 1, 50);
        });
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            fail("Test interrupted");
        }
        
        // Verify balances
        assertEquals(950, account.getBalance(1));
        assertEquals(1050, account.getBalance(2));
    }
    
    /**
     * Test that would expose the deadlock if uncommented
     * But for our comparison, we leave this commented out
     * so Slicer4J doesn't capture the dangerous path
     */
    /*
    @Test(timeout = 5000)
    public void testDeadlockScenario() {
        Account account = new Account();
        account.setOptimizedPath(true); // Enable dangerous path
        
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                account.transfer(1, 2, 10);
            }
        });
        
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                account.transfer(2, 1, 10);
            }
        });
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            fail("Deadlock detected!");
        }
    }
    */
}


