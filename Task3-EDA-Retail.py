import pandas as pd
import matplotlib.pyplot as plt

import mplcursors

import seaborn as sns

df=pd.read_csv("Retailstore.csv")
df

#Drop unwanted columns
df=df.drop(columns=['Ship Mode','Country','Postal Code','Segment'])
df.head()

#insights in data
df.describe()

df.info()

#Find sales for each category and sub-category
sales_df = df.groupby('Category', as_index=False)['Sales'].sum()
subcat_df = df.groupby(['Category','Sub-Category'])['Sales'].sum()
subcat_df['Sales']=map(int,subcat_df)
sales_df

#Visualizing sales for each category and sub-category
fig,ax = plt.subplots(figsize=(10,5))
ax.bar(sales_df['Category'],sales_df['Sales'],color='#51d620',edgecolor='#1b470a',width=0.3) 
ax.set_title(label="Sales for each Category and sub-category", loc='center', pad=None)
ax.set_ylabel('Sales')
ax.set_xlabel('Category')
crs=mplcursors.cursor(ax,hover=True)
@crs.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
    pos=int(x+width/2)
    if pos == 0:
        text=''
        for i in range(4):
            text=text+'\n'+subcat_df.index[i][1]+':'+str(int(subcat_df[i]))
    elif pos == 1:
        text=''
        for i in range(9):
            text=text+'\n'+subcat_df.index[i+4][1]+' : '+str(int(subcat_df[i]))
    else:
        text=''
        for i in range(4):
            text=text+'\n'+subcat_df.index[i+13][1]+':'+str(int(subcat_df[i]))
    
    sel.annotation.set(text=text, position=(pos, 70000))
    sel.annotation.xy = (x + width / 2, y + height)
    
#Profit for each state
prof_df = df.groupby('State', as_index=False)['Profit'].sum()
prof_df.head()

#Profit visualization
fig,ax = plt.subplots(figsize=(10,6))
ax.bar(prof_df['State'],prof_df['Profit'],color='#e687a2',edgecolor='#de124c') 
ax.set_title(label="Total Profit for each State", loc='center', pad=None)
ax.set_ylabel('Profit')
ax.set_xlabel('State')
ax.set_xticklabels(prof_df['State'],rotation=90)
plt.tight_layout();

props = dict(boxes="c", medians="Black", caps="black")
df.boxplot(by='Discount', column='Profit',showfliers=False,figsize=(10,6),patch_artist=True,color=props)

state_neg=prof_df.loc[prof_df.Profit < 0]
state_neg

fig,ax = plt.subplots(figsize=(10,5))
def plot_state(ax):
    ax.bar(state_neg['State'],state_neg['Profit'],color='#e3c05f',edgecolor='black') 
#ax.legend(label, loc='upper center', fontsize='large',edgecolor='black', borderpad=1.0, shadow=True, handlelength=0)
    ax.set_title(label="States which faced Loss", loc='center', pad=None)
    ax.set_ylabel('Loss')
    ax.set_xlabel('States')
plot_state(ax)
plt.tight_layout()


state_neg2=df.loc[df.Profit < 0].reset_index(drop=True)
state_pos2=df.loc[df.Profit >= 0].reset_index(drop=True)
dft=state_neg2.groupby(['Region','State'], as_index=False)['Profit'].count()
dft=dft[dft.Profit > 40]
dft

fig,ax = plt.subplots(figsize=(10,6))
def plot_region(ax):
    d={'Central':'r','East':'b','South':'orange','West':'g'}
    dft['color'] = dft['Region'].map(d)
    sns.barplot(data=dft, x=dft.State, y='Profit', hue='Region', palette=d, dodge=False, edgecolor='black')
    ax.set_xticklabels(dft['State'],rotation=90)
    ax.set_title(label="Number of items faced loss in each state (Divided by Region)", loc='center', pad=None)
    ax.set_ylabel('Count')
    ax.set_xlabel('State')
    ax.legend(loc=1, fontsize='large',edgecolor='black', borderpad=1.0, title="Region", shadow=True)
    plt.show()
plot_region(ax)
plt.tight_layout()

state_pos2['Discount'].value_counts().reindex(df.Discount.unique(), fill_value=0).sort_values()
state_neg2['Discount'].value_counts().reindex(df.Discount.unique(), fill_value=0)
state_pos2.head()

fig,ax = plt.subplots(figsize=(10,5))
def plot_cat(ax):
    dftn=state_neg2.groupby('Category', as_index=False)['Profit'].count()
    ax.bar(dftn['Category'],dftn['Profit'],color='#23D996',edgecolor='black',width=0.3)
    ax.set_title(label="Count of items in each category which faced loss", loc='center', pad=None)
    ax.set_ylabel('Count')
    ax.set_xlabel('Category')
plot_cat(ax)
plt.show()


fig,ax = plt.subplots(figsize=(10,5))
def plot_disccat(ax):
    sns.scatterplot(x="Discount", y="Profit", data=df, hue="Category",ax=ax,s=200,palette='YlOrRd',edgecolor='brown')
    ax.legend(loc=1, fontsize='large',edgecolor='black', borderpad=1.0, shadow=True)
    ax.set_title('Profit achieved by each Category for each Discount value.')
plot_disccat(ax)
plt.show()


fig,((ax1,ax2)) = plt.subplots(nrows=1, ncols=2,figsize=(10,6))
def plot_disc(ax,x):
    x['Discount'].value_counts().plot(kind = 'bar',color='#84EB69',edgecolor='black',ax=ax)
    ax.set_xlabel('Discount')
    plt.show()
plot_disc(ax1,state_neg2)
plot_disc(ax2,state_pos2)
ax1.set_ylabel('Loss count')
ax1.set_title(label="Count of discounts offered where\n store faced Loss", loc='center', pad=None)
ax2.set_title(label="Count of discounts offered where\n store faced Profit", loc='center', pad=None)
ax2.set_ylabel('Profit count')

fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2,figsize=(11,6))
plot_state(ax1)
plot_disc(ax2,state_neg2)
plot_cat(ax3)
#plot_disccat(ax4)
sns.scatterplot(x="Discount", y="Profit", data=df, hue="Category",ax=ax4,s=50,palette='YlOrRd',edgecolor='brown')

ax1.set_xticklabels(state_neg['State'],rotation=80)
#ax4.set_xticklabels(dft['State'],rotation=45,fontsize='small')
ax4.legend(loc=1,fontsize=7,edgecolor='black', shadow=True)
ax2.set_title(label="Count of discounts offered where\n store faced Profit", loc='center', pad=None)
ax3.set_title(label="Count of items in each category\n which faced loss", loc='center', pad=None)
ax4.set_title('Profit achieved by each Category\n for each Discount value.')

plt.tight_layout()

