/**
 * Your implementation of an ArrayQueue.
 *
 * @author Andy Huang
 * @version 1.0
 * @userid ahuang432
 * @GTID 904203756
 * <p>
 * Collaborators: LIST ALL COLLABORATORS YOU WORKED WITH HERE
 * <p>
 * Resources: LIST ALL NON-COURSE RESOURCES YOU CONSULTED HERE
 */
public class ArrayQueue<T> {

    /*
     * The initial capacity of the ArrayQueue.
     *
     * DO NOT MODIFY THIS VARIABLE.
     */
    public static final int INITIAL_CAPACITY = 9;

    /*
     * Do not add new instance variables or modify existing ones.
     */
    private T[] backingArray;
    private int front;
    private int size;

    /**
     * Constructs a new ArrayQueue.
     */
    public ArrayQueue() {
        backingArray = (T[]) new Object[INITIAL_CAPACITY];
        size = 0;
        front = 0;
    }

    /**
     * Adds the data to the back of the queue.
     * <p>
     * If sufficient space is not available in the backing array, resize it to
     * double the current length. When resizing, copy elements to the
     * beginning of the new array and reset front to 0.
     * <p>
     * Must be amortized O(1).
     *
     * @param data the data to add to the back of the queue
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void enqueue(T data) {
        if (data == null) {
            throw new IllegalArgumentException("cannot add null data to queue");
        }

        if (size >= backingArray.length) {
            enlargeCapacity();
        }

        int index = (front + size) % backingArray.length;
        backingArray[index] = data;
        size++;
    }

    /**
     * Removes and returns the data from the front of the queue.
     * <p>
     * Do not shrink the backing array.
     * <p>
     * Replace any spots that you dequeue from with null.
     * <p>
     * If the queue becomes empty as a result of this call, do not reset
     * front to 0.
     * <p>
     * Must be O(1).
     *
     * @return the data formerly located at the front of the queue
     * @throws java.util.NoSuchElementException if the queue is empty
     */
    public T dequeue() {
        if (size == 0) {
            throw new java.util.NoSuchElementException("queue is empty; no data to return");
        }

        // wraparound index
        int index = front % backingArray.length;
        T data = backingArray[index];
        backingArray[index] = null;
        front++;
        size--;
        return data;
    }

    /**
     * Returns the data from the front of the queue without removing it.
     * <p>
     * Must be O(1).
     *
     * @return the data located at the front of the queue
     * @throws java.util.NoSuchElementException if the queue is empty
     */
    public T peek() {
        if (size == 0) {
            throw new java.util.NoSuchElementException("empty queue");
        }
        return backingArray[front];
    }

    /**
     * Returns the backing array of the queue.
     * <p>
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the backing array of the queue
     */
    public T[] getBackingArray() {
        // DO NOT MODIFY THIS METHOD!
        return backingArray;
    }

    /**
     * Doubles the size of the backing array.
     * <p>
     * Creates a new array at double the size of the backing array.
     * Copies all elements of the old array into the new array and
     * sets the new array as the backing array.
     */
    private void enlargeCapacity() {
        T[] newArray = (T[]) new Object[size * 2];
        for (int index = 0; index < size; index++) {
            newArray[index] = backingArray[index];
        }
        backingArray = newArray;
    }

    /**
     * Returns the front index of the queue.
     * <p>
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the front index of the queue
     */
    public int getFront() {
        // DO NOT MODIFY THIS METHOD!
        return front;
    }

    /**
     * Returns the size of the queue.
     * <p>
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the size of the queue
     */
    public int size() {
        // DO NOT MODIFY THIS METHOD!
        return size;
    }
}
