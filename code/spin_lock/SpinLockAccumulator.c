// SpinLockAccumulator.c
#include <jni.h>
#include "SpinLockAccumulator.h" // This header will be generated by the `javah` tool

// Implementation of the native method
JNIEXPORT void JNICALL Java_SpinLockAccumulator_pauseInstruction(JNIEnv *env, jclass class) {
	int i=0;
    for(; i<50; ++i)
		// Inline assembly for the "pause" instruction, which is often used in spin-wait loops
    	__asm__ __volatile__ ("pause" ::: "memory");
}
