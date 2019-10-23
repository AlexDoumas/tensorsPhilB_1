
# imports. 
import numpy as np
import pylab as plt
from scipy import spatial

# create a bunch of roles and fillers such that cosine similarity will be -1 to 1 bounded. 
role1 = np.array([1,1,1,1,0,0,0,0,0,0,0,0])
role_05 = np.array([1,0,1,0,1,0,1,0,0,0,0,0])
role_orth = np.array([0,0,0,0,1,1,1,1,0,0,0,0])
role_inv = np.array([-1,-1,-1,-1,0,0,0,0,0,0,0,0])
roles = [role1, role_05, role_orth, role_inv]
filler1 = np.array([1,0,0,0,1,0,0,0,1,1,0,0])
filler_05 = np.array([0,1,0,0,0,1,0,0,1,1,0,0])
filler_orth = np.array([0,1,0,0,0,1,0,0,0,0,1,1])
filler_inv = np.array([-1,0,0,0,-1,0,0,0,-1,-1,0,0])
fillers = [filler1, filler_05, filler_orth, filler_inv]
# as above, but independent role and filler spaces. 
# role1 = np.array([1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# role_05 = np.array([1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# role_orth = np.array([0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# role_inv = np.array([-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# roles = [role1, role_05, role_orth, role_inv]
# filler1 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0])
# filler_05 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0])
# filler_orth = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1])
# filler_inv = np.array([0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,-1,0,0,0,-1,-1,0,0])
# fillers = [filler1, filler_05, filler_orth, filler_inv]



# to get cosine similarity, you can use the cosine function from the spatial.distance package and subtract from 1 (i.e., 1 - spatial.distance.cosine(role1,role_id)). 
# check that the roles and fillers you made fit the bill. 


# make an array of all filler similarities. 
filler_sims = []
for filler in fillers:
    # get that filler's similarity to filler1.
    sim = 1 - spatial.distance.cosine(filler1,filler)
    filler_sims.append(sim)

# get similarity of all tensors for all levels of filler similarity when role similarity is 1.
tensor_sims_role_sim_1 = []
for filler in fillers:
    # create tensors
    tens1 = np.tensordot(role1,filler1, axes=0)
    tens2 = np.tensordot(role1,filler, axes=0)
    tens_sim = 1 - spatial.distance.cosine(tens1.flatten(),tens2.flatten())
    tensor_sims_role_sim_1.append(tens_sim)

# get similarity of all tensors for all levels of filler similarity when role similarity is .5.
tensor_sims_role_sim_05 = []
for filler in fillers:
    # create tensors
    tens1 = np.tensordot(role1,filler1, axes=0)
    tens2 = np.tensordot(role_05,filler, axes=0)
    tens_sim = 1 - spatial.distance.cosine(tens1.flatten(),tens2.flatten())
    tensor_sims_role_sim_05.append(tens_sim)

# get similarity of all tensors for all levels of filler similarity when role similarity is 0.
tensor_sims_role_sim_00 = []
for filler in fillers:
    # create tensors
    tens1 = np.tensordot(role1,filler1, axes=0)
    tens2 = np.tensordot(role_orth,filler, axes=0)
    tens_sim = 1 - spatial.distance.cosine(tens1.flatten(),tens2.flatten())
    tensor_sims_role_sim_00.append(tens_sim)

# get similarity of all tensors for all levels of filler similarity when role similarity is -1.
tensor_sims_role_sim_neg1 = []
for filler in fillers:
    # create tensors
    tens1 = np.tensordot(role1,filler1, axes=0)
    tens2 = np.tensordot(role_inv,filler, axes=0)
    tens_sim = 1 - spatial.distance.cosine(tens1.flatten(),tens2.flatten())
    tensor_sims_role_sim_neg1.append(tens_sim)

# plot similarities on same graph.
tensor_sims_role_sim_1,=plt.plot(filler_sims,tensor_sims_role_sim_1, 'k-', linewidth=1.5, label='role similarity = 1.0')
tensor_sims_role_sim_05,=plt.plot(filler_sims,tensor_sims_role_sim_05, 'b-', linewidth=1.5, label='role similarity = 0.5')
tensor_sims_role_sim_00,=plt.plot(filler_sims,tensor_sims_role_sim_00, 'k--', linewidth=1.5, label='role similarity = 0.0')
tensor_sims_role_sim_neg1,=plt.plot(filler_sims,tensor_sims_role_sim_neg1, 'b--', linewidth=1.5, label='role similarity = -1.0')
plt.xlabel('filler similarity')
plt.ylabel('tensor similarity')
# set the range of the axes.
plt.axis([-1,1,-1,1])
plt.grid(False)
plt.legend([tensor_sims_role_sim_1, tensor_sims_role_sim_05, tensor_sims_role_sim_00, tensor_sims_role_sim_neg1], ['role similarity = 1', 'role similarity = .05', 'role similarity = 0', 'role similarity = -1'])
plt.show()

# now do the additive sims for synchrony. 
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
sync_sims_1 = []
for filler in fillers:
    # create bindings. 
    rb1 = role1 + filler1
    rb2 = role1 + filler
    rb_sim = 1 - spatial.distance.cosine(rb1,rb2)
    sync_sims_1.append(rb_sim)
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
sync_sims_05 = []
for filler in fillers:
    # create bindings. 
    rb1 = role1 + filler1
    rb2 = role_05 + filler
    rb_sim = 1 - spatial.distance.cosine(rb1,rb2)
    sync_sims_05.append(rb_sim)
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
sync_sims_00 = []
for filler in fillers:
    # create bindings. 
    rb1 = role1 + filler1
    rb2 = role_orth + filler
    rb_sim = 1 - spatial.distance.cosine(rb1,rb2)
    sync_sims_00.append(rb_sim)
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
sync_sims_neg1 = []
for filler in fillers:
    # create bindings. 
    rb1 = role1 + filler1
    rb2 = role_inv + filler
    rb_sim = 1 - spatial.distance.cosine(rb1,rb2)
    sync_sims_neg1.append(rb_sim)
    
# plot similarities on same graph.
sync_sims_1,=plt.plot(filler_sims,sync_sims_1, 'k-', linewidth=1.5, label='role similarity = 1.0')
sync_sims_05,=plt.plot(filler_sims,sync_sims_05, 'b-', linewidth=1.5, label='role similarity = 0.5')
sync_sims_00,=plt.plot(filler_sims,sync_sims_00, 'k--', linewidth=1.5, label='role similarity = 0.0')
sync_sims_neg1,=plt.plot(filler_sims,sync_sims_neg1, 'b--', linewidth=1.5, label='role similarity = -1.0')
plt.xlabel('filler similarity')
plt.ylabel('synchronous role-binding similarity')
# set the range of the axes.
plt.axis([-1,1,-1,1])
plt.grid(False)
plt.legend([sync_sims_1, sync_sims_05, sync_sims_00, sync_sims_neg1], ['role similarity = 1', 'role similarity = .05', 'role similarity = 0', 'role similarity = -1'])
plt.show()

# now do the additive sims for asynchrony. 
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
async_sims_1 = []
for filler in fillers:
    # create bindings. 
    rolesim = 1 - spatial.distance.cosine(role1,role1)
    fillersim = 1 - spatial.distance.cosine(filler1,filler)
    rb_sim = (rolesim + fillersim)/2.0
    async_sims_1.append(rb_sim)
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
async_sims_05 = []
for filler in fillers:
    # create bindings. 
    rolesim = 1 - spatial.distance.cosine(role1,role_05)
    fillersim = 1 - spatial.distance.cosine(filler1,filler)
    rb_sim = (rolesim + fillersim)/2.0
    async_sims_05.append(rb_sim)
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
async_sims_00 = []
for filler in fillers:
    # create bindings. 
    rolesim = 1 - spatial.distance.cosine(role1,role_orth)
    fillersim = 1 - spatial.distance.cosine(filler1,filler)
    rb_sim = (rolesim + fillersim)/2.0
    async_sims_00.append(rb_sim)
# get similarity of all role-bindings for all levels of filler similarity when role similarity is 1.
async_sims_neg1 = []
for filler in fillers:
    # create bindings. 
    rolesim = 1 - spatial.distance.cosine(role1,role_inv)
    fillersim = 1 - spatial.distance.cosine(filler1,filler)
    rb_sim = (rolesim + fillersim)/2.0
    async_sims_neg1.append(rb_sim)

# plot similarities on same graph.
async_sims_1,=plt.plot(filler_sims,async_sims_1, 'k-', linewidth=1.5, label='role similarity = 1.0')
async_sims_05,=plt.plot(filler_sims,async_sims_05, 'b-', linewidth=1.5, label='role similarity = 0.5')
async_sims_00,=plt.plot(filler_sims,async_sims_00, 'k--', linewidth=1.5, label='role similarity = 0.0')
async_sims_neg1,=plt.plot(filler_sims,async_sims_neg1, 'b--', linewidth=1.5, label='role similarity = -1.0')
plt.xlabel('filler similarity')
plt.ylabel('asynchronous role-binding similarity')
# set the range of the axes.
plt.axis([-1,1,-1,1])
plt.grid(False)
plt.legend([async_sims_1, async_sims_05, async_sims_00, async_sims_neg1], ['role similarity = 1', 'role similarity = .05', 'role similarity = 0', 'role similarity = -1'])
plt.show()





