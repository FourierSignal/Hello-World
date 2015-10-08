#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/platform_device.h>
#include <linux/gpio.h>
#include <linux/leds.h>
#include <linux/of_platform.h>
#include <linux/of_gpio.h>
#include <linux/slab.h>
#include <linux/workqueue.h>
#include <linux/module.h>
#include <linux/pinctrl/consumer.h>
#include <linux/err.h>
#include <linux/irq.h>
#include <linux/interrupt.h>

static struct timer_list led_timer;

#define MAX_LEDS 3
#define MAX_GPIO_PINS 3

static int gpio_ctrl_remove(struct platform_device *pdev);


struct gpio_pin_data{
        unsigned gpio;
		unsigned long flags;
		unsigned char *label;
        unsigned can_sleep;
        unsigned active_low;
        unsigned default_state;   /* default_state should be one of LEDS_GPIO_DEFSTATE_(ON|OFF|KEEP) */
};

struct gpio_ctrl_data{
//        const char *name; // ---???what&how to name this.
//        const char *default_trigger;
		struct led_classdev led_cdev;   //-----think wether to keep it here or seperate.
        unsigned int in_gpio;
        unsigned int out_gpio;
        unsigned int led_gpio;
		struct gpio_pin_data gpio_pindata_array[MAX_GPIO_PINS];
//   	struct gpio gpio_pin_data[3];   //decide need/not??		
//      unsigned int default_state : 2;       
    //    unsigned int active_low : 1;
  //      unsigned int retain_state_suspended : 1;
//		unsigned int default_state;
};

struct gpio_ctrl_platform_data {
        int num_leds;
        struct gpio_ctrl_data ctrlmodules[MAX_LEDS];
};

//struct gpio_ctrl_platform_data *priv=NULL;


void led_toggle_callback( unsigned long data )
{
 // printk( "led_toggle_callback (%ld).\n", jiffies );
//	printk("led-gpio=%d\n",gpio_get_value(priv->ctrlmodule[0].led_gpio));
	if(gpio_get_value(priv->ctrlmodule[0].led_gpio))
	gpio_set_value(priv->ctrlmodule[0].led_gpio,0);
	else
	gpio_set_value(priv->ctrlmodule[0].led_gpio,1);

	{
	int ret=0;
  	ret = mod_timer( &led_timer, jiffies + msecs_to_jiffies(2000) );
 	if(ret) printk("Error in mod_timer\n %d",ret);
	}
}

static irqreturn_t gpio_ctrl_ISR(int irq, void *dev_id)
{
	

	printk("gpio_ctrl_ISR: irq=%d\n",irq);
	if(irq == gpio_to_irq(priv->ctrlmodule[0].in_gpio))
	{
		/*
		printk("Interrupt on ON_LED mod\n");
		printk("led-gpio=%d\n",gpio_get_value(priv->ctrlmodule[0].led_gpio));	
		gpio_set_value(priv->ctrlmodule[0].led_gpio,1);
		printk("led-gpio=%d\n",gpio_get_value(priv->ctrlmodule[0].led_gpio));	
		return IRQ_HANDLED;
		*/
		{
		int ret=0;
	 	printk( "Starting timer to fire in 200ms (%ld)\n", jiffies );
  		ret = mod_timer( &led_timer, jiffies + msecs_to_jiffies(2000) );
 	 	if(ret) printk("Error in mod_timer\n %d",ret);
		return IRQ_HANDLED;
		}

	}
		return IRQ_NONE;
}


/*
include/linux/gpio.h
struct gpio {
 40         unsigned        gpio;
 41         unsigned long   flags;
 42         const char      *label;
 43 };
*/
//
//vi drivers/gpio/gpiolib.c 

/*
struct gpio_ctrl {
        const char *name;
        const char *default_trigger;
		struct led_classdev led_cdev;   //-----think wether to keep it here or seperate.
        unsigned        in_gpio;
        unsigned        out_gpio;
        unsigned        led_gpio;
        unsigned        active_low : 1;
        unsigned        retain_state_suspended : 1;
        unsigned        default_state : 2;
        // default_state should be one of LEDS_GPIO_DEFSTATE_(ON|OFF|KEEP) 
};
*/

static const struct of_device_id of_gpio_ctrl_match[] = {
        { .compatible = "gpio_ctrl", },
        {},
};


static int gpio_ctrl_probe(struct platform_device *pdev)
{
	struct gpio_ctrl_platform_data *pdata=NULL;
	struct gpio_ctrl_data *ctrlmodules = NULL;

	struct device_node *np=NULL, *child=NULL;
    struct pinctrl *pinctrl=NULL;
    unsigned int count=0;
	int  ret = 0;

//	struct gpio_ctrl_platform_data *priv;

	printk(KERN_ALERT "In gpio_ctrl_probe: \n");
{
	const char *devname;
 	devname = dev_name(&(pdev->dev));
	printk(KERN_ALERT "devname=%s\n",devname);
//	printk(KERN_ALERT "devname=%s\n",kobject_name(&(pdev->dev)->kobj);
	printk(KERN_ALERT "devname=%s\n",kobject_name(&( (pdev->dev.kobj))) );
}
    pinctrl = devm_pinctrl_get_select_default(&pdev->dev);		
    if (IS_ERR(pinctrl))
       dev_warn(&pdev->dev,"pins are not configured from the driver\n");
	printk(KERN_ALERT "pinctrl=%ld\n",PTR_ERR(pinctrl));

	pdata = devm_kzalloc(&pdev->dev, MAX_LEDS*sizeof(struct gpio_ctrl_platform_data),GFP_KERNEL);
	if (!pdata)
      return(-ENOMEM);

	np = pdev->dev.of_node;
    count = of_get_child_count(np);
        if (!count)
                return (-ENODEV);
	printk("child-count=%d\n",count);
    for_each_child_of_node(np, child){
	struct gpio_ctrl_data *ctrlmodule= &(pdata->ctrlmodules[pdata->num_leds++]);
    ctrlmodule->out_gpio = of_get_gpio(child, 0);
    ctrlmodule->in_gpio = of_get_gpio(child, 1);
    ctrlmodule->led_gpio = of_get_gpio(child, 2);

	printk("gpios--%d %d %d\n",ctrlmodule->out_gpio,ctrlmodule->in_gpio,ctrlmodule->led_gpio);
	ctrlmodule->name = of_get_property(child, "label", NULL) ? : child->name;
	  
	 ctrlmodule->led_cdev.name =of_get_property(child, "label", NULL) ? : child->name;
	printk("ctrlmodule->led_cdev.name=%s\n",ctrlmodule->led_cdev.name);

	printk("irq_no=%d\n",gpio_to_irq(ctrlmodule->in_gpio) );


	ret = gpio_request_one(ctrlmodule->out_gpio,GPIOF_OUT_INIT_LOW,ctrlmodule->name);
      if(ret < 0)
         return ret;


	ret = gpio_request_one( ctrlmodule->in_gpio,GPIOF_IN,ctrlmodule->name);  		
      if(ret < 0)
         return ret;

	ret = gpio_request_one( ctrlmodule->led_gpio,GPIOF_OUT_INIT_LOW,ctrlmodule->name);
      if(ret < 0)
        return ret;

	printk(KERN_ALERT "Gpio_ctrl:gpio_request_one\n");
{
		printk("irq_no=%d\n",gpio_to_irq(ctrlmodule->in_gpio) );
	ret = request_irq(gpio_to_irq(ctrlmodule->in_gpio),gpio_ctrl_ISR,IRQF_TRIGGER_RISING , "gpio_ctrl",NULL);
	if(ret != 0)
		printk("\n Request_irq Failed %d\n",ret);
};
	gpio_export(ctrlmodule->out_gpio,0);
	gpio_export(ctrlmodule->in_gpio,0);
	gpio_export(ctrlmodule->led_gpio,0);

	ret = led_classdev_register(&pdev->dev,&(ctrlmodule->led_cdev) );
    if(ret < 0)
	    return ret;
	}

	printk(KERN_ALERT "Gpio_ctrl:led_classdev_register\n");
	platform_set_drvdata(pdev, pdata);
   
	printk(KERN_ALERT "Gpio_ctrl:probe \n");
	
return 0;
}



static int gpio_ctrl_remove(struct platform_device *pdev)
{
	if((&(priv->ctrlmodule[0].led_cdev))!=NULL)
	 led_classdev_unregister(&(priv->ctrlmodule[0].led_cdev) );	
	else
	printk("led_classdev_unreg:Failed\n");

     gpio_unexport(priv->ctrlmodule[0].out_gpio);
	 gpio_unexport(priv->ctrlmodule[0].in_gpio);
	 gpio_unexport(priv->ctrlmodule[0].led_gpio);
		

	free_irq(gpio_to_irq(priv->ctrlmodule[0].in_gpio),NULL);

	gpio_free(priv->ctrlmodule[0].out_gpio );
	gpio_free(priv->ctrlmodule[0].in_gpio );
	gpio_free(priv->ctrlmodule[0].led_gpio );

printk("gpio_ctrl_remove: done\n");
         return 0;
}


static struct platform_driver gpio_ctrl_driver = {
        .probe          = gpio_ctrl_probe,
        .remove         = gpio_ctrl_remove,
        .driver         = {
                .name   = "gpio_ctrl_custom",
                .owner  = THIS_MODULE,
                .of_match_table = of_match_ptr(of_gpio_ctrl_match),
        },
};

static int __init gpio_ctrl_init(void)
{
	platform_driver_register(&gpio_ctrl_driver);
	
	setup_timer( &led_timer, led_toggle_callback, 0 );
printk("Timer setup done\n");
	
	printk(KERN_ALERT "Gpio_ctrl Drv Registered\n");
//	pr_debug("gpio_ctrl_init: successful\n");
return 0; 
}

static void  gpio_ctrl_exit(void)
{
	int ret=0;
	del_timer( &led_timer );
	platform_driver_unregister(&gpio_ctrl_driver);
	printk(KERN_ALERT "Gpio_ctrl Drv exit\n");

}
module_init(gpio_ctrl_init);
module_exit(gpio_ctrl_exit);
MODULE_LICENSE("GPL");



struct gpio_led {
328         const char *name;
329         const char *default_trigger;
330         unsigned        gpio;
331         unsigned        active_low : 1;
332         unsigned        retain_state_suspended : 1;
333         unsigned        default_state : 2;
334         /* default_state should be one of LEDS_GPIO_DEFSTATE_(ON|OFF|KEEP) */
335         struct gpio_desc *gpiod;
336 };

struct gpio_led_platform_data {
342         int             num_leds;
343         const struct gpio_led *leds;



-------------------------------------------------
 lt3593_led_probe:
 struct gpio_led_platform_data *pdata = dev_get_platdata(&pdev->dev);

  struct lt3593_led_data *leds_data;

  leds_data = devm_kzalloc(&pdev->dev,
145                         sizeof(struct lt3593_led_data) * pdata->num_leds,
146                         GFP_KERNEL);


for (i = 0; i < pdata->num_leds; i++) {
 ret = create_lt3593_led(&pdata->leds[i], &leds_data[i],
152                                       &pdev->dev);



  platform_set_drvdata(pdev, leds_data);

-------------------------------------------------------------------


