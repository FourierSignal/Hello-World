#include <stdio.h>
#include <stdlib.h>
typedef struct node_struct{
        int data;
        struct node_struct *next;
}node;

node *head_ptr = NULL;

node* append_node(node **head,int val)
{
  node *curr;
  node *last_node;
//  first = *head;
   printf("Append_list\n");

     last_node=(node *)malloc(sizeof(struct node_struct));
     last_node->data = val;
     last_node->next = NULL;

      if(*head == NULL)
       *head = last_node;
      else
      {
	  for(curr = *head; curr->next!= NULL; curr=curr->next)
  			;
      curr->next = last_node;
      }
  return (*head);
}

node* addnode_at_head(node **head,int val)
{

  node *first = (node *)malloc(sizeof(struct node_struct));
  first->data = val;
  first->next = NULL;

  if(*head == NULL)
     *head = first;
  else
  {
     first->next = (*head);
     (*head) = first;
  }
 
}

/*
best logic i found till now for delete node is 

1) handle case:  if head is NULL 
2) handle junking of head node as seperate case
3) handle junking of nodes other than head node seperately
     here dont junk:  curr  node.
     instead junk : curr->next  node
     this helps in skipping the last node case (deleting last node).
    
*/


node* delete_node(node **head,int val)
{
  node *curr;
  node *junk_node;
  printf("delete_node\n");

      if(*head == NULL)
       {
         printf("Head is NULL\n");
         //return *head;
         return NULL;
       }
      else if((*head)->data == val)
      {
        junk_node = (*head);
        (*head)=(*head)->next;
      }
      else
      {
      	//note : we can't generalize logic for deleting first node and deleting any other node
      	// or atleast we need to handle or check wether we are deleting first node.
      	/*
      	  for(curr = *head;(curr->next != NULL); curr=curr->next)
          {
             if(curr->data == val)
             {
                 if(*head == curr)
                 {
                    junk_node = curr;
                    *head = curr->next;
                     break;
                 }
                 else
                 {
                     junk_node = curr;
                     ??? here is the problem: how we handle prev pointer
                     break;
                 }
             }
          }
      	*/
      	
      	/*
      	  Even with prev we can't generalize logic)
      	  prev = *head;
      	  for(curr = *head;(curr->next != NULL); curr=curr->next)
      	  {
      	        if(curr->data == val)
      	        {
      	           junk_node = curr;
      	           prev->next = curr-> next; 
      	           // in head node case: this statement fails: 
      	           // head node case: (*head)->next = (*head)->next; won't skip the current node 
      	           // It replaces curr->next with same value => no effect
      	           break;
      	        }
      	        prev=curr;
      	  }
      	  free(junk_node);
      	  
      	*/
      	
        /*
      	  prev = *head;
      	  for(curr = *head;(curr->next != NULL) &&(curr->data==val); curr=curr->next)
      	     we need to handle head case.
      	     and also last node case.
      	     so better is to go for handling head seperately and junking curr->next node.
      	*/
      	
    	  for(curr = *head;(curr->next != NULL); curr=curr->next)
          {
             if(curr->next->data == val)
             {
                junk_node = curr->next;
                curr->next = curr->next->next;
                //here there is no problem with last node case
                //if junk_node is last node curr->next->next is NULL 
                //there is not a problem becuse we are dereferencing curr->next but not curr->next->next
                break;
             }
          }
       }
free(junk_node);
return (*head);
}


node* Insert_before_node(node **head,int val)
{
  node *curr;
  node *new_node;
  node *temp;
  printf("Insert_node\n");

      if(*head == NULL)
       {
         printf("Head is NULL\n");
         return *head;
       }

      new_node = (node *)malloc(sizeof(struct node_struct));
      printf("Enter value to be inserted\n");
      scanf("%d",&(new_node->data));
      new_node->next = NULL;
      if((*head)->data == val)
      {
        new_node->next = (*head);
        (*head)=new_node;
      }
      else
      {
    	  for(curr = *head;(curr->next != NULL); curr=curr->next)
          {
             if(curr->next->data == val)
             {
                temp = curr->next;
                curr->next = new_node;
                new_node->next = temp;
                break;
             }
          }
       }

return (*head);
}


node* Insert_after_node(node **head,int val)
{
  node *temp;
  node *new_node;
  node *curr;
  printf("Insert_After_a node\n");

      if(*head == NULL)
       {
         printf("Head is NULL\n");
         return *head;
       }
      new_node = (node *)malloc(sizeof(struct node_struct));
      printf("Enter value to be inserted\n");
      scanf("%d",&(new_node->data));
      new_node->next = NULL;
#if 0
   	  for(curr = *head;(curr->next != NULL); curr=curr->next)
      {
             if(curr->data == val)
             {
                temp = curr->next;
                curr->next = new_node;
                new_node->next = temp;
                break;
             }
       }
       if(curr->next==NULL)
       {
           curr->next = new_node;
       }
#endif
   	  for(curr = *head;(curr!= NULL); curr=curr->next)
      {
             if(curr->data == val)
             {

                temp = curr->next;
                curr->next = new_node;
                new_node->next = temp;
                break;
             }
       }

return (*head);
}

print_list(node *head)
{
   printf("print_list\n");
   node *curr;
   for(curr=head;curr!=NULL;curr=curr->next)
   {
    printf("|%d|--->",curr->data);
   }
   printf("NULL\n");
}

int main()
{
  char choice;
  int val;
printf(" %p \n",&head_ptr);

  printf("Enter A : add a node @End\n");
  printf("Enter B : add a node @head\n");
  printf("Enter I : Insert a node Before a node\n");
  printf("Enter J : Insert a node After a node\n");
  printf("Enter D: Delete a node \n");
  printf("Enter P: print list\n");
  printf("Enter Q: Quit\n");
while (1)
{

  printf("Enter choice \n");
  choice=getchar();  
  printf("choice=%d %c\n",choice,choice);
  switch(choice)
  {

       case 'A':  
           printf("Enter val to append\n");
           scanf("%d",&val);
           printf("val=%d\n",val);
           append_node(&head_ptr,val); 
           break;
       case 'B':
           printf("Enter val @ head\n");
           scanf("%d",&val);
           addnode_at_head(&head_ptr,val); 
           break;
       case 'D':
           printf("Enter val to be deleted\n");
           scanf("%d",&val);
           delete_node(&head_ptr,val);           
           break;
       case 'I':
           printf("Enter val before which node to be Inserted\n");
           scanf("%d",&val);getchar();getchar();getchar();
           Insert_before_node(&head_ptr,val);  
           break;
       case 'J':
           printf("Enter val after which nodeto be Inserted\n");
           scanf("%d",&val);getchar();getchar();getchar();
           Insert_after_node(&head_ptr,val);  
           break;        
       case 'P':
           print_list(head_ptr); 
           break; 
       case 'Q':
           exit(0);
           break;
       default:
           printf("Invalid choice\n");
              
   }
     getchar();getchar();getchar();
 }
return 0; 
}


//##################################################################################################################

Binary Tree



Algorithm:

1. if no root node , create node, Initialise left,right pointers to NULL, point root to the node.

2. if root node exist ,
   find val is left to node or right to node.
   if left , pass pointer to left pointer, val 
   if right, pass pointer to right pointer , val
   recursively


 void insert(node ** tree, int val)
 {
    node *temp = NULL;
    if(!(*tree))
    {
       temp = (node *)malloc(sizeof(node));
       temp->left = temp->right = NULL;
       temp->data = val;
       *tree = temp;
       return;
    }

    if(val < (*tree)->data)
    {
      insert(&(*tree)->left, val);
    }
    else if(val > (*tree)->data)
    {
      insert(&(*tree)->right, val);
    }
 }



 node* search(node ** tree, int val)
 {
    if(!(*tree))
    {
      return NULL;
    }
    if(val == (*tree)->data)
    {
       return *tree;
    }
    else if(val < (*tree)->data)
    {
       search(&((*tree)->left), val);
    }
    else if(val > (*tree)->data)
    {
      search(&((*tree)->right), val);
    }
 }


 void deltree(node * tree)
 {
   if(tree)
   {
      deltree(tree->left);
      deltree(tree->right);
      free(tree);
   }
 }






