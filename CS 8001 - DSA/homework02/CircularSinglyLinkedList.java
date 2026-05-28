/**
 * Your implementation of a CircularSinglyLinkedList without a tail pointer.
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
public class CircularSinglyLinkedList<T> {

    /*
     * Do not add new instance variables or modify existing ones.
     */
    private CircularSinglyLinkedListNode<T> head;
    private int size;

    /*
     * Do not add a constructor.
     */

    /**
     * Adds the data to the specified index.
     * <p>
     * Must be O(1) for indices 0 and size and O(n) for all other cases.
     *
     * @param index the index at which to add the new data
     * @param data  the data to add at the specified index
     * @throws java.lang.IndexOutOfBoundsException if index < 0 or index > size
     * @throws java.lang.IllegalArgumentException  if data is null
     */
    public void addAtIndex(int index, T data) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("index needs to be within size of linked list");
        }
        if (data == null) {
            throw new IllegalArgumentException("please provide non-null data");
        }

        if (index == 0) {
            addToFront(data);
            return;
        }


        CircularSinglyLinkedListNode<T> current = this.head;
        CircularSinglyLinkedListNode<T> previous = this.head;

        // navigate thru linked lists
        for (int i = 1; i <= index; i++) {
            previous = current;
            current = current.getNext();
        }
        CircularSinglyLinkedListNode<T> newNode = new CircularSinglyLinkedListNode<>(data, current);
        previous.setNext(newNode);

        size++;
    }

    /**
     * Adds the data to the front of the list.
     * <p>
     * Must be O(1).
     *
     * @param data the data to add to the front of the list
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void addToFront(T data) {
        if (data == null) {
            throw new IllegalArgumentException("please provide non-null data");
        }

        if (head == null) {
            head = new CircularSinglyLinkedListNode<>(data, null);
            head.setNext(head);
            size++;
            return;
        }

        CircularSinglyLinkedListNode<T> current = head;
        CircularSinglyLinkedListNode<T> newHead = new CircularSinglyLinkedListNode<>(data, head);

        while (current.getNext() != head) {
            current = current.getNext();
        }
        current.setNext(newHead);
        head = newHead;
        size++;
    }

    /**
     * Adds the data to the back of the list.
     * <p>
     * Must be O(1).
     *
     * @param data the data to add to the back of the list
     * @throws java.lang.IllegalArgumentException if data is null
     */
    public void addToBack(T data) {
        this.addAtIndex(size, data);
    }

    /**
     * Removes and returns the data at the specified index.
     * <p>
     * Must be O(1) for index 0 and O(n) for all other cases.
     *
     * @param index the index of the data to remove
     * @return the data formerly located at the specified index
     * @throws java.lang.IndexOutOfBoundsException if index < 0 or index >= size
     */
    public T removeAtIndex(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("index needs to be within size of linked list");
        }

        if (index == 0) {
            return removeFromFront();
        }

        CircularSinglyLinkedListNode<T> current = this.head;
        for (int i = 1; i < index; i++) {
            current = current.getNext();
        }
        CircularSinglyLinkedListNode<T> previous = current;
        current = current.getNext();
        CircularSinglyLinkedListNode<T> next = current.getNext();

        previous.setNext(next);
        size--;
        if (size == 0) {
            clear();
        }
        return current.getData();
    }

    /**
     * Removes and returns the first data of the list.
     * <p>
     * Must be O(1).
     *
     * @return the data formerly located at the front of the list
     * @throws java.util.NoSuchElementException if the list is empty
     */
    public T removeFromFront() {
        if (size == 0) {
            throw new java.util.NoSuchElementException("cannot remove element from an empty list");
        }

        CircularSinglyLinkedListNode<T> current = head;
        T oldHeadValue = head.getData();
        CircularSinglyLinkedListNode<T> newHead = head.getNext();

        while (current.getNext() != head) {
            current = current.getNext();
        }
        current.setNext(newHead);
        head = newHead;
        size--;
        if (size == 0) {
            clear();
        }
        return oldHeadValue;
    }

    /**
     * Removes and returns the last data of the list.
     * <p>
     * Must be O(n).
     *
     * @return the data formerly located at the back of the list
     * @throws java.util.NoSuchElementException if the list is empty
     */
    public T removeFromBack() {
        if (size == 0) {
            throw new java.util.NoSuchElementException("cannot remove element from an empty list");
        }
        return removeAtIndex(size - 1);
    }

    /**
     * Returns the data at the specified index.
     * <p>
     * Should be O(1) for index 0 and O(n) for all other cases.
     *
     * @param index the index of the data to get
     * @return the data stored at the index in the list
     * @throws java.lang.IndexOutOfBoundsException if index < 0 or index >= size
     */
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("index needs to be within size of linked list");
        }

        CircularSinglyLinkedListNode<T> current = this.head;
        for (int i = 1; i <= index; i++) {
            current = current.getNext();
        }
        return current.getData();
    }

    /**
     * Returns whether or not the list is empty.
     * <p>
     * Must be O(1).
     *
     * @return true if empty, false otherwise
     */
    public boolean isEmpty() {
        return size == 0;
    }

    /**
     * Clears the list.
     * <p>
     * Clears all data and resets the size.
     * <p>
     * Must be O(1).
     */
    public void clear() {
        head = null;
        size = 0;
    }

    /**
     * Removes and returns the last copy of the given data from the list.
     * <p>
     * Do not return the same data that was passed in. Return the data that
     * was stored in the list.
     * <p>
     * Must be O(n).
     *
     * @param data the data to be removed from the list
     * @return the data that was removed
     * @throws java.lang.IllegalArgumentException if data is null
     * @throws java.util.NoSuchElementException   if data is not found
     */
    public T removeLastOccurrence(T data) {
        if (data == null) {
            throw new IllegalArgumentException("data must be non-null");
        }

        CircularSinglyLinkedListNode<T> current = head;
        int index = 0;
        int indexToRemove = 0;
        boolean found = false;
        if (current == null) {
            throw new java.util.NoSuchElementException("linked list is empty");
        }

        while (true) {
            if (current.getData().equals(data)) {
                indexToRemove = index;
                found = true;
            }
            if (current.getNext() == head) {
                break;
            }
            index++;
            current = current.getNext();
        }

        if (!found) {
            throw new java.util.NoSuchElementException("data not found in linked list");
        }

        return removeAtIndex(indexToRemove);
    }

    /**
     * Returns an array representation of the linked list.
     * <p>
     * Must be O(n) for all cases.
     *
     * @return the array of length size holding all of the data (not the
     * nodes) in the list in the same order
     */
    public T[] toArray() {
        T[] arr = (T[]) new Object[size];
        CircularSinglyLinkedListNode<T> current = head;
        int i = 0;
        while (current != null) {
            arr[i] = current.getData();
            current = current.getNext();
            i++;
            if (current == head) {
                break;
            }
        }
        return arr;
    }

    /**
     * Returns the head node of the list.
     * <p>
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the node at the head of the list
     */
    public CircularSinglyLinkedListNode<T> getHead() {
        // DO NOT MODIFY!
        return head;
    }

    /**
     * Returns the size of the list.
     * <p>
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the size of the list
     */
    public int size() {
        // DO NOT MODIFY!
        return size;
    }
}
