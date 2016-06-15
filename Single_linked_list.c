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
  node *temp;
  node *first = (node *)malloc(sizeof(struct node_struct));
  first->data = val;
  first->next = NULL;

  if(*head == NULL)
     *head = first;
  else
  {
     temp = (*head);
     (*head) = first;
     first->next = temp;
  }
 
}


node* delete_node(node **head,int val)
{
  node *curr;
  node *junk_node;
  printf("delete_node\n");

      if(*head == NULL)
       {
         printf("Head is NULL\n");
         return *head;
       }
      else if((*head)->data == val)
      {
        junk_node = (*head);
        (*head)=(*head)->next;
      }
      else
      {
    	  for(curr = *head;(curr->next != NULL); curr=curr->next)
          {
             if(curr->next->data == val)
             {
                junk_node = curr->next;
                curr->next = curr->next->next;
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

